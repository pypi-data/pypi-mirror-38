#!/usr/bin/python3

"""List data (ad hoc code)."""

from dwi import Path


def _read(path):
    p = Path(path)
    for line in p.open():
        c, s = line.split()
        c = int(c)
        yield c, s


def _has_scans(t, lst):
    case, scan_num = t
    has_a = (case, scan_num+'a') in lst
    has_b = (case, scan_num+'b') in lst
    if has_a and has_b:
        return 'x'
    if has_a:
        return 'a'
    if has_b:
        return 'b'
    return '-'
