import os
import json
import csv
import re
import numpy as np
import pandas as pd
import torch
from skimage.morphology import label, remove_small_objects
from .config import config


def image_picker(root, path, channel='DAPI', failback=None):
    ext = ['jpg', 'jpeg', 'png', 'tif', 'tiff']
    ext += [x.upper() for x in ext]
    ext = tuple(ext)
    path = os.path.join(root, path, 'images')
    if not os.path.exists(path):
        return
    files = [f for f in os.listdir(path) if f.endswith(ext)]
    files.sort()
    def _isin(sub, default=None):
        assert isinstance(sub, list)
        for fn in files:
            if any(s in fn for s in sub):
                return fn
        return default
    def _r(fn):
        if not fn:
            return
        if isinstance(fn, list):
            return [os.path.join(path, f) for f in fn]
        return os.path.join(path, fn)
    rule = json.loads(config.get('channels', channel))
    assert isinstance(rule, list)
    if isinstance(rule[0], list):
        # nested rule
        fn = []
        for x in rule:
            fn.append(_isin(x))
        if not fn.count(None):
            return _r(fn)
    else:
        fn = _isin(rule)
        if fn is not None:
            return _r(fn)
    # no matched filename, check failback
    if isinstance(failback, str):
        return image_picker(root, path, failback)
    elif isinstance(failback, int):
        return _r(files[failback])
    return

# modified from https://www.kaggle.com/paulorzp/run-length-encode-and-decode
# note: the rle encoding is in vertical direction per Kaggle competition rule
# mask_id == -1 for pure semantic case; for differentiating instances case otherwise
def rle_decode(mask_id, mask_rle, shape):
    h, w = shape
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(h * w, dtype=np.uint16) if (mask_id != -1) else np.full(h * w, False)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = mask_id if (mask_id != -1) else True
    return img.reshape((w, h)).T

# merge ctc nuclei into semantic numpy array
def get_ctc_nuclei_array(csv_path, json_path, shape):
    df = pd.read_csv(csv_path, index_col=0, names=['ImageId', 'EncodedPixels'], delimiter=',', skiprows=1)
    try:
        with open(json_path) as f:
            data = json.load(f)
    except EnvironmentError:
        data = {}
    mask_ids = data.get('ctc', [])
    # mask_ids[:] = [x for x in mask_ids if x != 'ctc']
    nuclei = np.full(shape, False)
    for mask in mask_ids:
        rle = df.loc[mask, 'EncodedPixels']
        # print(rle)
        obj = rle_decode(-1, rle, shape)
        nuclei = np.logical_or(nuclei, obj)
    return nuclei

# merge all nuclei into instance-distinguishable numpy array
def get_nuclei_array(path, shape):
    csv_path = os.path.join(path, 'mask.csv')
    with open(csv_path) as f:
        reader = csv.reader(f)
        next(reader) #skip header
        nuclei = np.zeros(shape, dtype=np.uint16)
        for mask_id, rle in reader:
            match = re.search(r'mask_([0-9]+)', mask_id)
            mask_id = match[1]
            obj = rle_decode(mask_id, rle, shape)
            nuclei = np.maximum(nuclei, obj)
    return nuclei

def get_match_nuclei(path, prob_array):
    threshold = config['post'].getfloat('threshold')
    mask_csv = os.path.join(path, 'mask.csv')

    target = prob_array > threshold
    result = []
    with open(mask_csv) as f:
        d_reader = csv.DictReader(f)
        for line in d_reader:
            obj = rle_decode(-1, line['EncodedPixels'], target.shape)
            overlap = target & obj
            if overlap.sum() and ((overlap.sum() / obj.sum()) > 0.5):
                rows, cols = np.nonzero(overlap)
                prob = np.mean(prob_array[rows, cols])
                result.append((line['ImageId'], prob))
    return result

def write_ctc_prob(src_path, tgt_path, data):
    src_csv = os.path.join(src_path, 'mask.csv')
    tgt_csv = os.path.join(tgt_path, 'mask.csv')
    df = pd.read_csv(src_csv)
    if 'Label' not in df.columns:
        df['Prop'] = 0
        df['Label'] = ''
    # assign value to dataframe
    df = df.set_index('ImageId')
    for id, prob in data:
        df.at[id, 'Prob'] = prob
    df.to_csv(tgt_csv)

# copy from https://github.com/pytorch/examples/blob/master/imagenet/main.py#L139
class AverageMeter():
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

# copy from https://www.kaggle.com/aglotero/another-iou-metric
# y_pred & labels are all 'labelled' numpy arrays
def iou_metric(y_pred, labels, print_table=False):
    true_objects = len(np.unique(labels))
    pred_objects = len(np.unique(y_pred))

    intersection = np.histogram2d(labels.flatten(), y_pred.flatten(), bins=(true_objects, pred_objects))[0]

    # Compute areas (needed for finding the union between all objects)
    area_true = np.histogram(labels, bins = true_objects)[0]
    area_pred = np.histogram(y_pred, bins = pred_objects)[0]
    area_true = np.expand_dims(area_true, -1)
    area_pred = np.expand_dims(area_pred, 0)

    # Compute union
    union = area_true + area_pred - intersection

    # Exclude background from the analysis
    intersection = intersection[1:,1:]
    union = union[1:,1:]
    union[union == 0] = 1e-9

    # Compute the intersection over union
    iou = intersection / union

    # Precision helper function
    def precision_at(threshold, iou):
        matches = iou > threshold
        true_positives = np.sum(matches, axis=1) == 1   # Correct objects
        false_positives = np.sum(matches, axis=0) == 0  # Missed objects
        false_negatives = np.sum(matches, axis=1) == 0  # Extra objects
        tp, fp, fn = np.sum(true_positives), np.sum(false_positives), np.sum(false_negatives)
        return tp, fp, fn

    # Loop over IoU thresholds
    prec = []
    if print_table:
        print("\nThresh\tTP\tFP\tFN\tPrec.")
    for t in np.arange(0.5, 1.0, 0.05):
        tp, fp, fn = precision_at(t, iou)
        if (tp + fp + fn) > 0:
            p = tp / (tp + fp + fn)
        else:
            p = 0
        if print_table:
            print("{:1.3f}\t{}\t{}\t{}\t{:1.3f}".format(t, tp, fp, fn, p))
        prec.append(p)

    if print_table:
        print("AP\t-\t-\t-\t{:1.3f}".format(np.mean(prec)))
    return np.mean(prec)

def iou_mean(y_pred_in, y_true_in):
    y_pred_in = y_pred_in.to('cpu').detach().numpy()
    y_true_in = y_true_in.to('cpu').detach().numpy()
    batch_size = y_true_in.shape[0]
    metric = []
    for idx in range(batch_size):
        y_pred = label(y_pred_in[idx])
        y_true = label(y_true_in[idx] > 0)
        value = iou_metric(y_pred, y_true)
        metric.append(value)
    return np.mean(metric)

# checkpoint handling
def check_ckpt_dir():
    checkpoint_dir = os.path.join('.', 'checkpoint')
    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)

def ckpt_path(epoch=None):
    check_ckpt_dir()
    current_path = os.path.join('.', 'checkpoint', 'current.json')
    if epoch is None:
        if os.path.exists(current_path):
            with open(current_path) as infile:
                data = json.load(infile)
                epoch = data['epoch']
        else:
            return ''
    else:
        with open(current_path, 'w') as outfile:
            json.dump({
                'epoch': epoch
            }, outfile)
    return os.path.join('.', 'checkpoint', '{}.dat'.format(epoch))

def is_best_ckpt(epoch, iou_tr, iou_cv):
    check_ckpt_dir()
    best_json = os.path.join('.', 'checkpoint', 'best.json')
    best_iou_cv = best_iou_tr = 0
    if os.path.exists(best_json):
        with open(best_json) as infile:
            data = json.load(infile)
            best_iou_cv = data['iou_cv']
            best_iou_tr = data['iou_tr']
    best_iou_tr = max(0.35, best_iou_tr) # only save best checkpoint above certain IoU
    cv_threshold = 0.01 # tolerance of degraded CV IoU
    if iou_tr > best_iou_tr and iou_cv > best_iou_cv - cv_threshold:
        with open(best_json, 'w') as outfile:
            json.dump({
                'epoch': epoch,
                'iou_tr': iou_tr,
                'iou_cv': iou_cv,
            }, outfile)
        return True
    return False

# DataParallel will change model's class name to 'dataparallel' & prefix 'module.' to existing parameters.
# Here the saved checkpoint might or might not be 'DataParallel' model (e.g. might be trained with multi-GPUs or single GPU),
# handle this variation while loading checkpoint.
# Refer to:
#   https://github.com/pytorch/pytorch/issues/4361
#   https://github.com/pytorch/pytorch/issues/3805
#   https://stackoverflow.com/questions/44230907/keyerror-unexpected-key-module-encoder-embedding-weight-in-state-dict
def _extract_state_from_dataparallel(checkpoint_dict):
    from collections import OrderedDict
    new_state_dict = OrderedDict()
    for k, v in checkpoint_dict.items():
        if k.startswith('module.'):
            name = k[7:] # remove 'module.'
        else:
            name = k
        new_state_dict[name] = v
    return new_state_dict


def save_ckpt(model, optimizer, epoch, iou_tr, iou_cv):
    def do_save(filepath):
        torch.save({
            'epoch': epoch,
            'name': config['param']['model'],
            'model': model.state_dict(),
            'optimizer': optimizer.state_dict(),
        }, filepath)
    # check if best checkpoint
    if is_best_ckpt(epoch, iou_tr, iou_cv):
        filepath = os.path.join('.', 'checkpoint', 'best.dat')
        do_save(filepath)
    # save checkpoint per n epoch
    n_ckpt_epoch = config['train'].getint('n_ckpt_epoch')
    if epoch % n_ckpt_epoch == 0:
        filepath = ckpt_path(epoch)
        do_save(filepath)


def load_ckpt(model=None, optimizer=None, filepath=None):
    if filepath is None:
        filepath = ckpt_path()
    if not os.path.isfile(filepath):
        return 0 if model else (None, '')
    print("Loading checkpoint '{}'".format(filepath))
    if torch.cuda.is_available():
        # Load all tensors onto previous state
        checkpoint = torch.load(filepath)
    else:
        # Load all tensors onto the CPU
        checkpoint = torch.load(filepath, map_location=lambda storage, loc: storage)
    if optimizer:
        try:
            optimizer.load_state_dict(checkpoint['optimizer'])
        except ValueError as err:
            print('[WARNING]', err)
            print('[WARNING] optimizer not restored from last checkpoint, continue without previous state')
    if model:
        model.load_state_dict(_extract_state_from_dataparallel(checkpoint['model']))
        return checkpoint['epoch']
    else:
        # build model based on checkpoint
        from .model import build_model
        assert 'name' in checkpoint, "Abort! No model name in checkpoint, use ckpt.py to convert first"
        model_name = checkpoint['name']
        model = build_model(model_name)
        model.load_state_dict(_extract_state_from_dataparallel(checkpoint['model']))
        return model, model_name

def freeze_ckpt(src, dest):
    model, model_name = load_ckpt(filepath=src)
    model.eval()
    for param in model.parameters():
        param.requires_grad = False
    torch.save({
        'copyright': '© 2018 AIxMed, Inc. All Rights Reserved',
        'name': model_name,
        'model': model.state_dict()
    }, dest)

# cut-off probabibility to semantic segmentations
def prob_to_segment(raw_bodies):
    threshold=config['param'].getfloat('threshold')
    bodies = raw_bodies > threshold
    return bodies

# Run-length encoding stolen from https://www.kaggle.com/rakhlin/fast-run-length-encoding-python
def rle_encoding(y):
    dots = np.where(y.T.flatten() == 1)[0]
    run_lengths = []
    prev = -2
    for b in dots:
        if (b>prev+1): run_lengths.extend((b + 1, 0))
        run_lengths[-1] += 1
        prev = b
    return run_lengths

def segment_to_instances(y):
    remove_objects = config['post'].getboolean('remove_objects')
    min_object_size = config['post'].getint('min_object_size')

    y = partition_instances(y)
    if remove_objects:
        y = remove_small_objects(y, min_size=min_object_size)
    return y

def segment_to_rles(y):
    instances, _ = segment_to_instances(y)
    idxs = np.unique(instances) # sorted, 1st is background (e.g. 0)
    if len(idxs) == 1:
        yield []
    else:
        for idx in idxs[1:]:
            yield rle_encoding(instances == idx)

# TODO: REVISE FOR CTC CASE
def partition_instances(bodies, edges=None, markers=None):
    return