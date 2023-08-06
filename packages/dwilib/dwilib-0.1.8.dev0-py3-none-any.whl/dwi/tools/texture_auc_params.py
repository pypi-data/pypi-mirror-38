#!/usr/bin/python3

"""Select best params (for that T2w lesion-wise detection thingy)."""

import fileinput
import json

import numpy as np
import pandas as pd

from dwi.files import Path
# from dwi.job import Memory
import dwi.util

# memory = Memory()


# def main_old():
#     stats = [get_feat_stats(x) for x in data_all]
#     print('Features:', len(stats))
#     stats = sorted(stats, key=lambda x: (
#         x['auc_median'],
#         x['auc_mean'],
#         ))
#     s = (
#         '{threshold} {cases:2} {param:30} '
#         '{auc_median:{f}} {auc_mean:{f}} '
#         '{auc_five} '
#         )
#     for d in stats:
#         # print(threshold, mode, param, len(d), auc_mean, auc_median)
#         # print(d)
#         print(s.format(**d, f='.2f'))


# def get_feat_stats_old(data):
#     """Produce stats for each feature."""
#     threshold = data[0]['threshold']
#     mode = data[0]['mode']
#     param = data[0]['param']
#     assert all(x['threshold'] == threshold for x in data)
#     assert all(x['mode'] == mode for x in data)
#     assert all(x['param'] == param for x in data)
# 
#     aucs = [x['auc'] for x in data]
#     nnegs = [x['nneg'] for x in data]
#     nposs = [x['npos'] for x in data]
#     nvoxs = [x['nneg'] + x['npos'] for x in data]
# 
#     return dict(
#         threshold=threshold,
#         mode=mode,
#         param=param,
#         cases=len(data),
#         # aucs=aucs,
#         auc_mean=np.mean(aucs),
#         auc_median=np.median(aucs),
#         # auc_five=dwi.util.fivenum(aucs),
#         auc_five=dwi.util.fivenums(aucs, fmt='.2f'),
#         nneg_median=round(np.median(nnegs)),
#         npos_median=round(np.median(nposs)),
#         nvox_median=round(np.median(nvoxs)),
#         )


# @memory.cache
def read_data(path):
    p = Path(path)
    with p.open() as fp:
        data_all = json.load(fp)
    df = pd.DataFrame(data_all)
    return df


def preprocess_dataframe(df):
    # Drop unused columns.
    # cols = 'nboot ci1 ci2 flipped nles npos nneg nposles scores scan'.split()
    cols = 'nboot flipped nles nposles scores scan'.split()
    df = df.drop(cols, axis=1)
    # Select subset.
    df = df[df['mode'] == 'T2w-std'].drop('mode', axis=1)
    df = df[df['threshold'] == '0+0'].drop('threshold', axis=1)
    # # Drop missing AUC values.
    # df = df[~df.auc.isnull()]
    # # Add columns.
    # df['auc_diff'] = np.abs(df.auc_a - df.auc_b)  # AUC difference.
    # df['nprostate_a'] = df.nneg_a + df.npos_a  # Prostate voxels, a.
    # df['nprostate_b'] = df.nneg_b + df.npos_b  # Prostate voxels, b.
    # df['npos_rel_a'] = df.npos_a / df.nprostate_a  # Relative positives, a.
    # df['npos_rel_b'] = df.npos_b / df.nprostate_b  # Relative positives, b.
    # Normalize column order.
    df = df.sort_index(axis=1)
    return df


# @memory.cache
def get_stats(df):
    aucs = [(df[df['param'] == x].auc.median(), x) for x in df.param.unique()]
    aucs.sort(reverse=True)
    return dict(aucs=aucs)


def main():
    # path = '/mri/data/out/texture_auc-nobs-json-T2w-all-grouped.txt'
    path = '/mri/data/out/texture_auc-nobs-json-T2w-all-slurped.txt'
    df = read_data(path)  # TODO: Use pd.read_json()
    df = preprocess_dataframe(df)
    print(len(df), list(df.columns))
    # df = df.sort_values('auc')
    # print(df.tail(n=10))
    stats = get_stats(df)
    for auc, param in stats['aucs'][:50]:
        print('{:.3f} {}'.format(auc, param))


if __name__ == '__main__':
    main()
