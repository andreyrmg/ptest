__author__ = 'andrey'

from ptest.checklib import check, ok, read_ints


def run(inf, outf, ansf):
    inf.skip_int()
    k = inf.next_int()
    for a, b, i in read_ints(outf, ansf, k):
        check(a, b, i)
    return ok()