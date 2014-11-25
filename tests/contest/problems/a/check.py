__author__ = 'andrey'

from ptest.checklib import check, read_lines, ok


def run(inf, outf, ansf):
    n = inf.next_int()
    for a, b, i in read_lines(outf, ansf, n):
        check(a, b, i)
    return ok()