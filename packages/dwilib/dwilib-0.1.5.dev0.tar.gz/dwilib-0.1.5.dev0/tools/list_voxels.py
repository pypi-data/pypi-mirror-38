#!/usr/bin/python3

"""List prostate voxels with labels and pmap, tmap values.

Quoting IM:

I have chosen the PCa patients to include in the LPO and TLPO CV
experiment. The criteria for choosing the patients is:
- The patient only have high risk tumors in prostate peripheral zone (PZ).

Please, compute  ADCm Mean,  ADCm 11-gabor(1,0.3,mean), ADCk Mean, ADCk
11-gabor(1,0.3,mean), K Mean and K 11-gabor(1,0.3,mean).
So in total 6 features and label the voxels  1 for cancer and -1 for
non-cancer.

These are the patients numbers:
# 6, 7, 15, 16,17, 20, 21, 39, 25, 30, 41, 55, 60, 61, 66, 79, 81 (Use
scan A).
and I also need patients #56, 57, 65 (I think these patients have only
one scan... hopefully the masks are correct)
"""

from collections import OrderedDict
import logging

import numpy as np
import pandas as pd

import dwi.dataset
import dwi.mask
import dwi.util
from dwi.compat import param_to_tspec
from dwi.job import Memory
# from dwi.job import Parallel, delayed

memory = Memory()
# memory.clear()

MODES = """
DWI-Mono-ADCm
DWI-Mono-ADCm
DWI-Kurt-ADCk
DWI-Kurt-ADCk
DWI-Kurt-K
DWI-Kurt-K
""".split()

PARAMS = """
1-raw(mean)
11-gabor(1,0.3,mean)
1-raw(mean)
11-gabor(1,0.3,mean)
1-raw(mean)
11-gabor(1,0.3,mean)
""".split()

CASES = """
6 7 15 16 17 20 21 39 25 30 41 55 60 61 66 79 81
56 57 65
""".split()


# @memory.cache
def read_lesion_tmaps(modes, case, scan, params, pmask, slice_indices=None):
    """Read tmaps."""
    if slice_indices is not None:
        pmask = pmask[slice_indices].copy()
    lst = []
    for mode, param in zip(modes, params):
        tspec = param_to_tspec(param)
        print('Reading:', param, tspec)
        d = dict(ondisk=True, params=[param])
        if tspec.method == 'raw':
            d['params'] = [0]
        tmap = dwi.dataset.read_tmap(mode, case, scan, tspec, **d)
        # tmap = tmap.get_params([param]).copy()
        logging.debug(tmap.shape)
        if slice_indices is not None:
            tmap = tmap[slice_indices].copy()
        tmap = tmap[pmask]
        lst.append(tmap)
    return lst


# @memory.cache
def read_target(mode, case, scan, lesions, pmask):
    """Target has prostate as 0, lesion as 1."""
    lmask = dwi.dataset.read_lesion_masks(mode, case, scan, lesions,
                                          only_largest=True)
    slice_indices = list(range(len(lmask)))
    maxfirst = True
    if maxfirst:
        slice_indices = [dwi.mask.Mask3D(lmask).max_slices()[0]]
        lmask = lmask[slice_indices].copy()
        pmask = pmask[slice_indices].copy()

    target = np.zeros_like(lmask, dtype=np.int8)
    target[lmask] = 1
    target = target[pmask]
    return target, slice_indices


def read_data(modes, params, case, scan, lesions):
    pmask = dwi.dataset.read_prostate_mask(modes[0], case, scan)
    y, slice_indices = read_target(modes[0], case, scan, lesions, pmask)
    tmaps = read_lesion_tmaps(modes, case, scan, params, pmask,
                              slice_indices=slice_indices)
    tmaps = np.array(tmaps)
    X = tmaps[:, :, 0].T
    nsamples, nfeats = X.shape
    return dict(X=X, y=y, slice_ix=slice_indices[0],
                nsamples=nsamples, nfeats=nfeats)


def main():
    modes = [dwi.ImageMode(x) for x in MODES]
    params = PARAMS
    samplelist = 'i'
    cases = [int(x) for x in CASES]
    # cases = cases[:2]
    print('Working on:', modes, params, samplelist, cases)
    ds = dwi.dataset.Dataset(modes[0], samplelist, cases=cases)
    data = [dict(case=c, scan=s, lesions=l) for c, s, l in ds.each_image_id()]
    print('Initial:', len(data), data)
    for d in data:
        print(d)
        d.update(read_data(modes, params, d['case'], d['scan'], d['lesions']))
        print(d['X'].shape, d['y'].shape, d['nsamples'], d['nfeats'])
    print(sum(x['X'].shape[0] for x in data))
    df = pd.DataFrame()
    for d in data:
        for x, target in zip(d['X'], d['y']):
            o = OrderedDict()
            o['case'] = d['case']
            o['scan'] = d['scan']
            o['label'] = target
            o['slice_ix'] = d['slice_ix']
            for m, p, f in zip(modes, params, x):
                o['{}_{}'.format(m, p)] = f
            df = df.append(pd.DataFrame([o]))
    path = 'out/voxel_list.csv'
    df.to_csv(path)


if __name__ == '__main__':
    main()
