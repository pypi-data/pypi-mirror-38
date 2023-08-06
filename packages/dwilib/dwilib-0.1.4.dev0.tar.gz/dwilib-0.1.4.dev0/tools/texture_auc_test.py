#!/usr/bin/python3

"""Lesion-wise AUC, apply the Wilcoxon signed-rank test."""

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html

from collections import OrderedDict
import fileinput
from itertools import product
import json
import logging
import sys

import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
from statsmodels.stats import descriptivestats

from dwi.files import Path
from dwi.job import Memory, Parallel, delayed
import dwi.plot
import dwi.stats
import dwi.util

memory = Memory()


def valid_lines_from_stream(fp=sys.stdin):
    """Read and yield lines that are neither empty nor comments."""
    return filter(None, (dwi.files.sanitize_line(x) for x in fp))


def each_line(files=None):
    """Read each line using fileinput module. Pathlike objects are accepted."""
    if files is not None:
        files = [str(x) for x in files]
    lines = fileinput.input(files=files)
    return filter(None, (dwi.files.sanitize_line(x) for x in lines))


def parse_line(line):
    try:
        d = json.loads(line)
        d['mode'] = d['mode'].split('-')[-1]  # E.g. DWI-Mono-ADCm -> ADCm.
        d['index'] = d['scan'][1]  # E.g. 1a -> a.
        assert d['index'] in 'ab', d
        return d
    except ValueError:
        logging.error('Could not parse line: %s', line)
        return None


def parse_object(obj):
    if 'auc' not in obj:
        logging.warning('No AUC: %s', obj)
        return None
    if obj['param'].startswith('all-'):
        logging.warning('Skipping feature: %s', obj)
        return None
    try:
        key = obj['threshold'], obj['mode'], obj['param']
        value = {(obj['case'], obj['index']): obj['auc']}
        return key, value
    except KeyError as e:
        logging.error('Invalid mapping: %s', obj)
        raise


def slurp_objects(objs):
    """Take a sequence of objects and build a dict of them."""
    aucs = {}
    for k, v in filter(None, (parse_object(x) for x in objs)):
        aucs.setdefault(k, {}).update(v)
    return aucs


def read_input(lines=None):
    if lines is None:
        lines = valid_lines_from_stream()
    return slurp_objects(filter(None, (parse_line(x) for x in lines)))


def read_dataframe(files=None):
    lines = each_line(files=files)
    def get_dicts():
        # for d in filter(None, (parse_line(x) for x in lines)):
        #     yield d
        yield from filter(None, (parse_line(x) for x in lines))
    return pd.DataFrame(get_dicts())


def r(value, n=3):
    """Round a scalar or elements of sequence."""
    if np.isscalar(value):
        return round(value, n)
    return [r(x, n=n) for x in value]


@memory.cache
def get_test_results(a, b):
    a = np.asanyarray(a)
    b = np.asanyarray(b)
    diffs = a - b
    test = {}
    if not np.all(a == b):
        test['M'] = r(descriptivestats.sign_test(diffs))
        test['U'] = r(stats.mannwhitneyu(a, b))
        test['W'] = r(stats.wilcoxon(a, b))
        try:
            d = dwi.stats.wilcoxon_signed_rank_test(diffs)
            test['WR'] = {k: r(v) for k, v in d.items()}
        except Exception as e:
            logging.exception('Diffs: %s', diffs)
    return test


def get_result(v):
    cases = sorted(set(x[0] for x in v))
    aucs = np.array([
        [v[(x, 'a')] for x in cases],
        [v[(x, 'b')] for x in cases]
        ])
    auc_mn = np.mean(aucs, axis=1)
    auc_md = np.median(aucs, axis=1)
    diffs = aucs[0] - aucs[1]
    diff_mn = np.mean(diffs)
    diff_md = np.median(diffs)

    data = dict(
        n=len(cases),
        aucs=aucs,
        mean=r(auc_mn),
        median=r(auc_md),
        diff_mean=r(diff_mn),
        diff_median=r(diff_md),
        )
    test = get_test_results(aucs[0], aucs[1])
    return dict(data=data, test=test)


def each_result(aucs):
    """Calculate test results."""
    items = sorted(aucs.items())
    with Parallel() as parallel:
        results = parallel(delayed(get_result)(v) for k, v in items)
    for (k, v), result in zip(items, results):
        d = OrderedDict()
        d['key'] = dict(threshold=k[0], mode=k[1], param=k[2])
        d.update(result)
        yield d


def get_aucs(results, t, m):
    for x in results:
        if (x['key']['threshold'], x['key']['mode']) == (t, m):
            aucs = np.array(x['data']['aucs'])
            assert aucs.shape[0] == 2, aucs.shape
            return aucs


def plot_aucs_param(results, path):
    thresholds = sorted({x['key']['threshold'] for x in results})
    modes = sorted({x['key']['mode'] for x in results})
    # logging.warning('## %s, %s, %s', thresholds, modes, path)
    # aucs_it = (get_aucs(results, t, m) for t, m in product(thresholds, modes))
    # titles = ['{}, {}'.format(t, m) for t, m in product(thresholds, modes)]
    # plt_it = dwi.plot.generate_plots(nrows=len(thresholds), ncols=len(modes),
    #                                  titles=titles, path=path)
    # for plt, aucs in zip(plt_it, aucs_it):
    #     plt.rcParams['savefig.dpi'] = '50'
    #     # x = list(range(len(aucs[0])))
    #     # plt.plot(x, aucs[0], x, aucs[1])
    #     # plt.hist([aucs[0], aucs[1]], bins=10, range=(0.5, 1), histtype='step')

    # def each_value_as_dict():
    #     for t, m in product(thresholds, modes):
    #         aucs = get_aucs(results, t, m)
    #         if any(np.mean(x) >= 0.8 for x in aucs):
    #             for i, a in enumerate(aucs, 1):
    #                 for v in a:
    #                     yield dict(threshold=t, mode=m, scan=i, AUC=v)
    # df = pd.DataFrame(each_value_as_dict())
    # if df.empty:
    #     return
    # sns.set_style('whitegrid')
    # d = dict(
    #     col='mode',
    #     size=4,
    #     aspect=.7,
    #     col_order=['ADCm', 'ADCk', 'K'],
    #     ylim=(.5, 1),
    #     )
    # g = sns.FacetGrid(df, **d)
    # d = dict(
    #     # order=['ADCm', 'ADCk', 'K'],
    #     bw=.2,
    #     cut=0,
    #     scale='count',
    #     # inner='quartile',
    #     inner='stick',
    #     split=True,
    #     linewidth=2,
    #     palette='Set2',
    #     )
    # g.map(sns.violinplot, 'threshold', 'AUC', 'scan', **d)
    # # g.map(sns.stripplot, 'threshold', 'AUC', 'scan', jitter=True, size=3)
    # # g.map(sns.swarmplot, 'threshold', 'AUC', 'scan', split=True, palette='Set2')
    # g.despine(left=True)
    # g.add_legend(title='scan')
    # g.savefig(str(path.with_suffix('.vln.png')))
    # g.fig.clear()
    # ##
    # def each_value_as_dict():
    #     for t, m in product(thresholds, modes):
    #         aucs = get_aucs(results, t, m)
    #         for a, b in aucs.T:
    #             yield dict(threshold=t, mode=m, AUC1=a, AUC2=b)
    # df = pd.DataFrame(each_value_as_dict())
    # sns.set_style('whitegrid')
    # data = df[df.threshold=='0+0']
    # ax = sns.kdeplot(data['AUC1'], data['AUC2'], cmap='Reds')
    # data = df[df.threshold=='3+3']
    # ax = sns.kdeplot(data['AUC1'], data['AUC2'], cmap='Blues')
    # ax.figure.savefig(str(path.with_suffix('.kde.png')))
    # ax.figure.clear()
    # ##
    def each_value_as_dict():
        for t, m in product(thresholds, modes):
            aucs = get_aucs(results, t, m)
            if any(np.mean(x) >= 0.8 for x in aucs):
                absdiff = np.abs(aucs[0] - aucs[1])
                for v in absdiff:
                    yield dict(threshold=t, mode=m, absdiff=v)
    df = pd.DataFrame(each_value_as_dict())
    if df.empty:
        return
    sns.set_style('whitegrid')
    d = dict(
        col='mode',
        size=4,
        aspect=.7,
        col_order=['ADCm', 'ADCk', 'K'],
        # ylim=(0, .5),
        ylim=(0, 50),
        xlim=(0, .5),
        )
    g = sns.FacetGrid(df, **d)
    d = dict(
        # order=['ADCm', 'ADCk', 'K'],
        # bw=.2,
        cut=0,
        # scale='count',
        # inner='quartile',
        # inner='stick',
        # split=True,
        linewidth=2,
        palette='Set2',
        )
    # g.map(sns.violinplot, 'threshold', 'absdiff', **d)
    g.map(sns.distplot, 'absdiff', kde=False, rug=True)
    g.despine(left=True)
    g.add_legend(title='scan')
    g.savefig(str(path.with_suffix('.absdiff.png')))
    g.fig.clear()


def plot_param(results, param):
    lst = [x for x in results if x['key']['param'] == param]
    plot_aucs_param(lst, Path('tmp/aucs_{}.png'.format(param)))


def plot_aucs(results):
    # for param in {x['key']['param'] for x in results}:
    #     lst = [x for x in results if x['key']['param'] == param]
    #     plot_aucs_param(lst, 'tmp/aucs_{}.png'.format(param))
    params = sorted(set(x['key']['param'] for x in results))
    with Parallel() as parallel:
        parallel(delayed(plot_param)(results, x) for x in params)


def write_output(results):
    # def sorted_by(seq, *keys, **kwargs):
    #     def key(item):
    #         return [item[x] for x in keys]
    #     return sorted(seq, key=key, **kwargs)
    # for d in sorted(results, key=lambda x: x['t'], reverse=True):
    # results = sorted_by(results, 'threshold', 'param')
    for d in results:
        del d['data']['aucs']
        print(dwi.util.dump_json(d, sort_keys=None))


def preprocess_dataframe(df):
    # Drop unused columns.
    # cols = 'nboot ci1 ci2 flipped nles npos nneg nposles scores scan'.split()
    # cols = 'nboot ci1 ci2 flipped nles nposles scores scan'.split()
    cols = 'nboot flipped nles nposles scores scan'.split()
    df = df.drop(cols, axis=1)
    # Drop missing AUC values.
    df = df[~df.auc.isnull()]
    # Make AUC repetitions as separate columns.
    a = df[df['index'] == 'a'].drop('index', axis=1)
    b = df[df['index'] == 'b'].drop('index', axis=1)
    cols = 'threshold param mode case'.split()
    df = pd.merge(a, b, on=cols, suffixes=['_a', '_b'])
    # Add columns.
    df['auc_diff'] = np.abs(df.auc_a - df.auc_b)  # AUC difference.
    df['nprostate_a'] = df.nneg_a + df.npos_a  # Prostate voxels, a.
    df['nprostate_b'] = df.nneg_b + df.npos_b  # Prostate voxels, b.
    df['npos_rel_a'] = df.npos_a / df.nprostate_a  # Relative positives, a.
    df['npos_rel_b'] = df.npos_b / df.nprostate_b  # Relative positives, b.
    # Normalize column order.
    df = df.sort_index(axis=1)
    return df


def main():
    # aucs = read_input()
    # results = list(each_result(aucs))
    # # aucs = {k: v for k, v in aucs.items() if 'gabor' in k[-1]}
    # plot_aucs(results)
    # # plot_aucs([x for x in results if 'gabor' in x['key']['param']])
    # write_output(results)

    df = read_dataframe()
    df = preprocess_dataframe(df)

    df = df[df['threshold'] == '0+0']
    # df = df[df['mode'] == 'ADCm']
    # df = df[df['param'] == '5-stats(mean)']

    # print(df.shape)
    # print(df.columns)
    # print(df.describe())

    # outpath = 'auc_data_raw.csv'
    outpath = 'auc_data_raw_largestonly.csv'
    df.to_csv(outpath)

    # g = sns.jointplot(x='auc_a', y='auc_b', data=df)
    # g.savefig('auc_scatter.png')
    # g.fig.clear()
    # g = sns.jointplot(x='npos_rel_a', y='npos_rel_b', data=df)
    # g.savefig('nposrel_scatter.png')
    # g.fig.clear()


if __name__ == '__main__':
    main()
