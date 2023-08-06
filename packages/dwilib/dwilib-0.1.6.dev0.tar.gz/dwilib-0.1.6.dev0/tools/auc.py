#!/usr/bin/python3

"""ROC AUC."""

from functools import lru_cache
from itertools import product
# import logging

import numpy as np

import dwi.dataset
import dwi.image
from dwi.job import Parallel, delayed
import dwi.stats
import dwi.util


@lru_cache(maxsize=16)
def read_pmap(mode, case, scan):
    path = dwi.paths.pmap_path(mode, case, scan)
    return dwi.image.Image.read(path, dtype=np.float32)


@lru_cache(maxsize=16)
def read_lesion_mask(mode, case, scan, lesion):
    path = dwi.paths.mask_path(mode, 'lesion', case, scan,
                               lesion=lesion.index+1)
    return dwi.files.read_mask(path)


@lru_cache()
def read_sample(mode, case, scan, lesion, avg=np.mean):
    pmap = read_pmap(mode, case, scan)
    mask = read_lesion_mask(mode, case, scan, lesion)
    return np.asscalar(avg(pmap[mask]))


def process_all(dataset, threshold, which='ab'):
    print('Mode: {}'.format(dataset.mode))
    print('Samplelist: {}'.format(dataset.samplelist))
    print('Scans: {}'.format(which))
    lst = list(dataset.each_lesion())
    if which:
        lst = [(c, s, l) for c, s, l in lst if s[1] in which]
    labels = [l.score > threshold for c, s, l in lst]
    print('Samples: {}: {}'.format(len(lst),
          ', '.join('({},{},{})'.format(*x) for x in lst)))
    print('Labels: {}: {}: {}'.format(len(labels), sum(labels),
          ''.join(str(int(x)) for x in labels)))

    # values = [read_sample(dataset.mode, *x) for x in lst]
    with Parallel(verbose=1) as parallel:
        values = parallel(delayed(read_sample)(dataset.mode, *x) for x in lst)
    print('Values: {}: {}'.format(len(values), dwi.util.fivenums(values)))

    scaler = dwi.stats.scale_minmax
    values = scaler(values)
    d = dwi.stats.roc_auc(labels, values, autoflip=True)
    print('Result: {auc:.2}'.format(**d))


def main():
    modes = [dwi.ImageMode(x) for x in ['DWI-Mono-ADCm']]
    samplelist = 'bothscansonly'
    thresholds = [dwi.GleasonScore(x) for x in ['3+3']]
    cases = None
    # cases = list(range(10))
    whiches = ['ab', 'a', 'b']

    for mode, threshold, which in product(modes, thresholds, whiches):
        dataset = dwi.dataset.Dataset(mode, samplelist, cases=cases)
        process_all(dataset, threshold, which=which)


if __name__ == '__main__':
    main()
