#!/usr/bin/python3

"""Lesion-wise AUC."""

# for each (case, scan, feature):
#     calculate AUC: lesion vs. non-lesion prostate voxels
#     calculate AUC: GS>3+3 lesion vs. non-lesion prostate voxels
#     calculate AUC: GS>3+4 lesion vs. non-lesion prostate voxels

from itertools import product
import logging

import numpy as np

import dwi.conf
import dwi.dataset
import dwi.doit
import dwi.files
import dwi.mask
import dwi.paths
import dwi.patient
import dwi.stats
import dwi.util
from dwi.job import Memory
# from dwi.job import Parallel, delayed

# SCALER = dwi.stats.scale_standard
SCALER = dwi.stats.scale_minmax

memory = Memory()


def parse_args():
    """Parse command-line arguments."""
    p = dwi.conf.get_parser(description=__doc__)
    p.add('-m', '--modes', nargs='+', type=dwi.ImageMode,
          default=[
              'DWI-Mono-ADCm',
              'DWI-Kurt-ADCk', 'DWI-Kurt-K',
              # 'T2w-std',
              ],
          help='imaging modes')
    p.add('-t', '--thresholds', nargs='+', type=dwi.GleasonScore,
          default=['0+0', '3+3'],
          help='classification thresholds (maximum negative)')
    p.add('--nboot', type=int, default=0,
          help='number of bootstraps (try 2000)')
    p.add('-s', '--samplelist', default='all',
          help='samplelist identifier')
    p.add('-c', '--cases', nargs='+', type=int,
          help='cases to include, if not all')
    return p.parse_args()


def read_lesion_tmap(mode, case, scan, lesions, tspec):
    """Return positive voxels, negative voxels, and parameter names."""
    img = dwi.dataset.read_tmap(mode, case, scan, tspec)
    pmask = dwi.dataset.read_prostate_mask(mode, case, scan)
    lmask = dwi.dataset.read_lesion_masks(mode, case, scan, lesions,
                                          only_largest=True)
    slice_indices = [-1]
    maxfirst = True
    if maxfirst:
        slice_indices = [dwi.mask.Mask3D(lmask).max_slices()[0]]
        img = img[slice_indices].copy()
        pmask = pmask[slice_indices].copy()
        lmask = lmask[slice_indices].copy()

    pos = img[pmask & lmask, :]
    neg = img[pmask & ~lmask, :]
    params = img.params
    if params == ['0']:
        params = ['{tspec.winsize}-{tspec.method}'.format(tspec=tspec)]
    return pos, neg, params, slice_indices[0]


def each_image_tmap(mode, case, scan, lesions):
    """Yield lesion voxels, non-lesion voxels, name for each feature."""
    for tspec in dwi.doit.texture_methods_winsizes(mode, 'lesion'):
        pos, neg, params, slice_ix = read_lesion_tmap(mode, case, scan,
                                                      lesions, tspec)
        for i, param in enumerate(params):
            yield pos[:, i], neg[:, i], param, slice_ix


def process_image(pos, neg, nboot):
    """Process an image."""
    labels, values = dwi.stats.posneg_to_labelsvalues(pos, neg)
    values = SCALER(values)
    return dwi.stats.roc_auc(labels, values, autoflip=True, nboot=nboot)


def test_order_change(values, f, msg):
    """Test how much transforming an array with f affects their order.
    For example:
        _, _x = dwi.stats.posneg_to_labelsvalues(pos, neg)
        test_order_change(_x, SCALER, s.format(**d))
    """
    before = np.argsort(values)
    values = f(values)
    after = np.argsort(values)
    eq = (before == after)
    if not np.alltrue(eq):
        n = eq.size
        good = np.count_nonzero(eq)
        bad = n - good
        s = 'Order change: {:.3f} {}/{} {}'.format(bad/n, bad, n, msg)
        logging.error(s)


def process_dataset(dataset, nboot, threshold):
    """Process a dataset."""
    logging.info('Mode: %s', dataset.mode)
    logging.info('Samplelist: %s', dataset.samplelist)
    r = dict(mode=str(dataset.mode), nboot=nboot, threshold=str(threshold))
    for case, scan, lesions in dataset.each_image_id():
        pos_lesions = tuple(x for x in lesions if x.score > threshold)
        r.update(case=case, scan=scan,
                 nles=len(lesions), nposles=len(pos_lesions),
                 scores=','.join(str(x.score) for x in lesions))
        if not pos_lesions:
            # yield r
            continue
        for pos, neg, param, slice_ix in each_image_tmap(dataset.mode, case,
                                                         scan, pos_lesions):
            r.update(param=param, npos=len(pos), nneg=len(neg),
                     slice_ix=slice_ix)
            # r.update(ci1=np.nan, ci2=np.nan)
            r.update(process_image(pos, neg, nboot))
            yield r


def main():
    """Main."""
    args = parse_args()
    datasets = (dwi.dataset.Dataset(x, args.samplelist, cases=args.cases)
                for x in args.modes)
    for dataset, threshold in product(datasets, args.thresholds):
        for r in process_dataset(dataset, args.nboot, threshold):
            print(dwi.util.dump_json(r))


if __name__ == '__main__':
    main()
