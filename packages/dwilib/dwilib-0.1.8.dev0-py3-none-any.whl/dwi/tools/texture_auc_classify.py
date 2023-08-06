#!/usr/bin/python3

"""Classify texture data voxel-wise."""

import logging

import numpy as np

from sklearn import svm
from sklearn import preprocessing

import dwi.dataset
import dwi.util
from dwi.compat import param_to_tspec
from dwi.job import Memory
from dwi.job import Parallel, delayed
from dwi.types import ImageMode

dwi.job._parallel_defaults['n_jobs'] = -1
memory = Memory()

PARAMS = """
19-glcm(ASM,1,mean)
19-glcm(energy,1,mean)
19-glcm(energy,1,alt)
19-glcm(ASM,1,alt)
19-glcm(ASM,2,alt)
19-glcm(energy,2,alt)
19-glcm(homogeneity,4,mean)
19-glcm(homogeneity,4,alt)
19-glcm(homogeneity,3,mean)
19-glcm(homogeneity,3,alt)
19-glcm(ASM,2,mean)
19-glcm(energy,2,mean)
19-glcm(dissimilarity,3,mean)
19-glcm(dissimilarity,3,alt)
19-glcm(energy,3,alt)
19-glcm(ASM,3,alt)
23-glcm(ASM,1,alt)
23-glcm(energy,1,alt)
23-glcm(energy,1,mean)
23-glcm(ASM,1,mean)
15-glcm(dissimilarity,3,mean)
15-glcm(dissimilarity,3,alt)
19-glcm(energy,3,mean)
23-glcm(ASM,2,mean)
19-glcm(energy,4,alt)
19-glcm(ASM,4,alt)
19-glcm(ASM,3,mean)
23-glcm(energy,2,mean)
23-glcm(ASM,2,alt)
23-glcm(energy,2,alt)
35-gabor(3,0.2,absmean)
19-glcm(energy,4,mean)
35-gabor(3,0.2,mag)
""".split()


def get_params(n):
    """Get parameter list to use."""
    # params = [
    #     '19-glcm(ASM,1,mean)',
    #     '19-glcm(energy,1,mean)',
    #     '19-glcm(homogeneity,4,mean)',
    #     '35-gabor(3,0.2,absmean)',
    #     ]
    params = []
    params += PARAMS[:n]
    # params += PARAMS[-n:]
    return params


@memory.cache
def read_lesion_tmaps(mode, case, scan, params, pmask):
    """Read tmaps."""
    lst = []
    for param in params:
        tspec = param_to_tspec(param)
        # print('Reading:', param, tspec)
        d = dict(ondisk=True, params=[param])
        if tspec.method == 'raw':
            d['params'] = [0]
        tmap = dwi.dataset.read_tmap(mode, case, scan, tspec, **d)
        # tmap = tmap.get_params([param]).copy()
        logging.debug(tmap.shape)
        tmap = tmap[pmask]
        lst.append(tmap)
    return lst


@memory.cache
def read_target(mode, case, scan, lesions, pmask):
    """Target has background as -1, prostate as 0, lesion as 1."""
    lmask = dwi.dataset.read_lesion_masks(mode, case, scan, lesions)
    target = np.zeros_like(lmask, dtype=np.int8)
    target[lmask] = 1
    target = target[pmask]
    return target


def read_data(mode, params, case, scan, lesions):
    pmask = dwi.dataset.read_prostate_mask(mode, case, scan)
    tmaps = read_lesion_tmaps(mode, case, scan, params, pmask)
    tmaps.append(np.ones_like(tmaps[0]))  # Add dummy feature.
    tmaps = np.array(tmaps)
    X = tmaps[:, :, 0].T
    y = read_target(mode, case, scan, lesions, pmask)
    nsamples, nfeats = X.shape
    return dict(X=X, y=y, nsamples=nsamples, nfeats=nfeats)


def split_data(data, ratio=0.8):
    """Split data list to train and test."""
    i = round(ratio * len(data))
    return data[:i], data[i:]


# @memory.cache
# def split(X, y, step=10):
#     """Split data to training and testing set."""
#     test_mask = np.zeros_like(y, dtype=np.bool)
#     test_mask[::step] = True
#     X_train = X[~test_mask]
#     X_test = X[test_mask]
#     y_train = y[~test_mask]
#     y_test = y[test_mask]
#     return X_train, X_test, y_train, y_test


@memory.cache
def train(X, y, params=None):
    print('Training:', X.shape, y.shape, params)
    X = preprocessing.scale(X)
    clf = svm.SVC()
    if params is None:
        params = dict(kernel='linear')
    clf.set_params(**params).fit(X, y)
    return clf


def classify(clf, X, y):
    X = preprocessing.scale(X)
    result = clf.predict(X)
    score = np.count_nonzero(result == y) / y.size
    return dict(score=score)


# @memory.cache
# def get_result(X, y):
#     X_train, X_test, y_train, y_test = split(X, y, step=5)
#     clf = train(X_train, y_train)
#     return dict(result=classify(clf, X_test, y_test))


# def process_image(mode, params, d):
#     d = dict(d, **read_data(mode, params, **d))
#     d = dict(d, **get_result(d['X'], d['y']))
#     return d


def main():
    mode = ImageMode('T2w-std')
    samplelist = 'all'
    threshold = '0+0'
    # threshold = '3+3'
    print('Working on:', mode, samplelist, threshold)
    params = get_params(5)
    print('Params:', len(params), params)
    # cases = [42]
    # cases = list(range(9))
    cases = list(range(40))
    ds = dwi.dataset.Dataset(mode, samplelist, cases=cases)
    data = [dict(case=c, scan=s, lesions=l) for c, s, l in ds.each_image_id()]
    print('Initial:', len(data), data)

    # Filter out low-score lesions.
    def is_pos(lesion):
        return lesion.score > threshold
    data = [dict(x, lesions=list(filter(is_pos, x['lesions']))) for x in data]
    data = [x for x in data if x['lesions']]
    print('Filtered:', len(data), data)

    # data = [dict(x, **read_data(mode, params, **x)) for x in data]
    # data = [dict(x, **get_result(x['X'], x['y'])) for x in data]

    # with Parallel(verbose=30) as parallel:
    #     args = mode, params
    #     data = parallel(delayed(process_image)(*args, x) for x in data)

    # print('Score:', dwi.util.fivenums([x['score'] for x in data], fmt='.3f'))
    # s = '{case}-{scan} {lesions} ({nsamples},{nfeats}) {score:.3f}'
    # for d in data:
    #     print(' ', s.format(**d))

    ####

    # data = [dict(x, **read_data(mode, params, **x)) for x in data]
    with Parallel(verbose=50) as parallel:
        f = memory.cache(read_data)
        lst = parallel(delayed(f)(mode, params, **x) for x in data)
    data = [dict(a, **b) for a, b in zip(data, lst)]

    data_train, data_test = split_data(data, ratio=0.5)
    # data_train = [dict(x, X=preprocessing.scale(x['X'])) for x in data_train]
    print('Splitted:', len(data_train), len(data_test))
    X_train = np.concatenate([x['X'] for x in data_train])
    y_train = np.concatenate([x['y'] for x in data_train])

    ##
    _step = 5
    X_train, y_train = X_train[::_step], y_train[::_step]
    ##

    clf = train(X_train, y_train, params=dict(kernel='linear', max_iter=100))
    print('Classifier:', clf)
    # data_test = [dict(x, score=classify(clf, x['X'], x['y'])) for x in
    #              data_test]
    with Parallel(verbose=50) as parallel:
        # f = memory.cache(classify)
        f = classify
        lst = parallel(delayed(classify)(clf, x['X'], x['y']) for x in
                       data_test)
    data_test = [dict(a, **b) for a, b in zip(data, lst)]

    print('Score:', dwi.util.fivenums([x['score'] for x in data_test],
                                      fmt='.3f'))
    s = '{case}-{scan} {lesions} ({nsamples},{nfeats}) {score:.3f}'
    for d in data_test:
        print(' ', s.format(**d))


if __name__ == '__main__':
    main()
