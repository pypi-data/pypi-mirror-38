#!/usr/bin/python3

"""Check repetitions for anomalies by comparing masks."""

import logging

import numpy as np
import pandas as pd
from scipy import stats

import dwi.conf
import dwi.dataset
from dwi.job import Memory
import dwi.util

memory = Memory()
HIGHLIGHTED = [14, 17, 27, 29, 41, 54, 63, 69, 74, 8]


def parse_args():
    """Parse command-line arguments."""
    p = dwi.conf.get_parser(description=__doc__)
    p.add('-m', '--modes', nargs='+', type=dwi.ImageMode,
          default=[
              'DWI',
              # 'DWI-Mono-ADCm',
              # 'DWI-Kurt-ADCk', 'DWI-Kurt-K',
              # 'T2w-std',
              ],
          help='imaging modes')
    p.add('-s', '--samplelist', default='all',
          help='samplelist identifier')
    p.add('-c', '--cases', nargs='+', type=int,
          help='cases to include, if not all')
    return p.parse_args()


def process_dataset(ds):
    """Process a dataset."""
    logging.info('Mode: %s', ds.mode)
    logging.info('Samplelist: %s', ds.samplelist)
    for p in ds.each_patient():
        for scan in p.scans:
            pmask = dwi.dataset.read_prostate_mask(ds.mode, p.num, scan)
            pmbb = pmask[pmask.mbb()].shape
            # pcentroid = tuple(round(x, 1) for x in pmask.centroid())
            pcentroid = tuple(pmask.centroid())
            for lesion in p.lesions:
                lmask = dwi.dataset.read_lesion_mask(ds.mode, p.num, scan,
                                                     lesion)
                lmbb = lmask[lmask.mbb()].shape
                # lcentroid = tuple(round(x, 1) for x in lmask.centroid())
                lcentroid = tuple(lmask.centroid())
                assert np.all(pmask.spacing == lmask.spacing), (pmask.spacing,
                                                                lmask.spacing)
                out = dict()
                out['mode'] = str(ds.mode)
                out['case'] = p.num
                out['nles'] = len(p.lesions)
                out['scan'], out['rep'] = scan  # Separate number, repetition.
                out['spacing'] = tuple(round(x, 3) for x in pmask.spacing)
                out['pvol'] = np.count_nonzero(pmask)
                out['pcentroid'] = pcentroid
                out['pmbb'] = pmbb
                out['lesion'] = lesion.index
                out['score'] = str(lesion.score)
                out['lvol'] = np.count_nonzero(lmask)
                out['lcentroid'] = lcentroid
                out['lmbb'] = lmbb
                yield dict(out)


@memory.cache
def read_dataframe(modes, samplelist, cases):
    datasets = (dwi.dataset.Dataset(x, samplelist, cases=cases) for x in modes)
    outs = (out for ds in datasets for out in process_dataset(ds))
    # for out in outs:
    #     print(dwi.util.dump_json(out, sort_keys=None))
    df = pd.DataFrame(outs)
    return df


def int_perhaps(x):
    """Convert number to int but only if its decimal part is zero."""
    return x if (x % 1) else int(x)


def round_msd(x, n=2):
    """Round to n most significant digits. Return int if possible."""
    return int_perhaps(round(x, -int(round(np.log10(x))) + n - 1)) if x else 0


def preprocess_dataframe(df):
    """Preprocess dataframe."""
    def r(x, ndigits=1):
        return np.round(x, ndigits)
    def distance(a, b, spacing=(1, 1, 1)):
        return dwi.util.distance(a, b, spacing=spacing)
    def volume(shape, spacing=(1, 1, 1)):
        return np.prod(np.multiply(shape, spacing))
    def diff(a, b):
        return r(abs(a - b), 3)
    def diff_rel(a, b):
        return r(abs(a - b) / abs(a), 2)

    # Number of slices.
    df['pslices'] = [x.pmbb[0] for x in df.itertuples()]
    df['lslices'] = [x.lmbb[0] for x in df.itertuples()]

    # Convert shapes to metric.
    for col in 'pcentroid lcentroid pmbb lmbb'.split():
        df[col] = [r(np.multiply(getattr(x, col), x.spacing)) for x
                   in df.itertuples()]
    # Convert scalars to metric.
    for col in 'pvol lvol'.split():
        df[col] = [r(getattr(x, col) * np.prod(x.spacing)) for x in
                   df.itertuples()]

    # Add lesion distance from prostate (by centroid).
    df['ldist'] = [distance(x.lcentroid, x.pcentroid) for x in df.itertuples()]
    # MBB volume.
    df['pmbb_vol'] = [volume(x.pmbb) for x in df.itertuples()]
    df['lmbb_vol'] = [volume(x.lmbb) for x in df.itertuples()]
    # Volume / MBB.
    df['pvolpermbb'] = [x.pvol / x.pmbb_vol for x in df.itertuples()]
    df['lvolpermbb'] = [x.lvol / x.lmbb_vol for x in df.itertuples()]
    # Lesion / prostate volume.
    df['lvolperpvol'] = [x.lvol / x.pvol for x in df.itertuples()]

    # # Round.
    # for col in 'pcentroid lcentroid pmbb lmbb'.split():
    #     df[col] = [[round_msd(y) for y in getattr(x, col)] for x in
    #                df.itertuples()]
    # for col in 'pvol lvol pmbb_vol lmbb_vol'.split():
    #     df[col] = [round_msd(getattr(x, col)) for x in df.itertuples()]

    # Merge repetitions as separate columns on same row.
    original_length = len(df)
    a = df[df['rep'] == 'a'].drop('rep', axis=1)
    b = df[df['rep'] == 'b'].drop('rep', axis=1)
    cols = 'mode case scan nles lesion score spacing'.split()
    df = a.merge(b, on=cols, suffixes=['_a', '_b'])
    assert original_length == len(df) * 2, (original_length, len(df))

    # Add difference between number of slices.
    df['pslices_diff'] = [diff(x.pslices_a, x.pslices_b) for x in df.itertuples()]
    df['lslices_diff'] = [diff(x.lslices_a, x.lslices_b) for x in df.itertuples()]
    df['pslices_diff_rel'] = [diff_rel(x.pslices_a, x.pslices_b) for x in df.itertuples()]
    df['lslices_diff_rel'] = [diff_rel(x.lslices_a, x.lslices_b) for x in df.itertuples()]
    # Add difference between lesion distances.
    df['ldist_diff'] = [diff(x.ldist_a, x.ldist_b) for x in df.itertuples()]
    df['ldist_diff_rel'] = [diff_rel(x.ldist_a, x.ldist_b) for x in df.itertuples()]
    # Add difference between prostate volumes and lesion volumes.
    df['pvol_diff'] = [diff(x.pvol_a, x.pvol_b) for x in df.itertuples()]
    df['lvol_diff'] = [diff(x.lvol_a, x.lvol_b) for x in df.itertuples()]
    df['pvol_diff_rel'] = [diff_rel(x.pvol_a, x.pvol_b) for x in df.itertuples()]
    df['lvol_diff_rel'] = [diff_rel(x.lvol_a, x.lvol_b) for x in df.itertuples()]
    df['pvolpermbb_diff'] = [diff(x.pvolpermbb_a, x.pvolpermbb_b) for x in df.itertuples()]
    df['lvolpermbb_diff'] = [diff(x.lvolpermbb_a, x.lvolpermbb_b) for x in df.itertuples()]

    # Normalize column order.
    df = df.sort_index(axis=1)
    return df


def add_auc_data(df, path='auc_data.csv'):
    auc_data = pd.read_csv(path)
    assert set(df.case) == set(auc_data.case)
    cols = 'case auc_a auc_b auc_diff'.split()
    df = df.merge(auc_data[cols], on='case')
    df['hl'] = [x.case in HIGHLIGHTED for x in df.itertuples()]
    return df


def corr(df):
    """Correlations."""
    def f(a, b, m):
        methods = dict(r=stats.spearmanr, t=stats.kendalltau)
        g = methods[m]
        try:
            # print(type(g(a, b)[0]))
            return tuple(round(float(x), 2) for x in g(a, b))
        except ValueError:
            return None

    aucs = df['auc_diff']
    r = {k: f(aucs, v, 'r') for k, v in df.items()}
    t = {k: f(aucs, v, 't') for k, v in df.items()}
    return r, t


def plot(df):
    ca = ['r' if x else 'b' for x in df['hl']]
    cb = ['y' if x else 'g' for x in df['hl']]
    # plt.scatter(df['auc_diff'], df['lvol_a'], c=ca)
    # plt.scatter(df['auc_diff'], df['lvol_b'], c=cb)


def main():
    """Main."""
    args = parse_args()
    # datasets = (dwi.dataset.Dataset(x, args.samplelist, cases=args.cases)
    #             for x in args.modes)
    # outs = (out for ds in datasets for out in process_dataset(ds))
    # for out in outs:
    #     print(dwi.util.dump_json(out, sort_keys=None))
    df = read_dataframe(args.modes, args.samplelist, args.cases)
    df = preprocess_dataframe(df)
    df = add_auc_data(df)
    r, t = corr(df)
    # df = df[df['hl'] == True]
    print(df)

    # Compare incorrect 5-mean with correct 1-raw (not much difference).
    # assert (df_mean.case == df_raw.case).all()
    # corr_mean, corr_raw = corr(df_mean), corr(df_raw)
    # for (mk, mv), (rk, rv) in zip(corr_mean[0].items(), corr_raw[0].items()):
    #     print({mk, rk}, mv, rv, sep='\t')

    # cols = 'case lesion auc_a auc_b auc_diff'.split()
    # df = pd.merge(df_mean[cols], df_raw[cols], on=cols[:2])
    # cols = 'case auc_a_x auc_b_x auc_a_y auc_b_y'.split()
    # df.sort_values('case')[cols].sort_values('auc_a_x')


if __name__ == '__main__':
    main()
