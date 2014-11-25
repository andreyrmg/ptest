from contextlib import contextmanager
import sys

from ptest.result import Result


__author__ = 'andrey'


class PresentationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class WrongAnswerError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Reader(object):
    def __init__(self, source, output=False):
        self._source = source
        self._output = output
        self._line = ''
        self._len = 0
        self._pos = 0
        self._next()

    def _next_line(self):
        self._line = self._source.readline()
        if not self._line and self._output:
            raise PresentationError('Unexpected end of file')
        self._len = len(self._line)
        self._pos = 0

    def _next(self):
        if self._pos < len(self._line):
            self._pos += 1
        else:
            self._next_line()

    @property
    def cur(self):
        return self._line[self._pos] if self._pos < self._len else ''

    def skip_ws(self):
        while self.cur.isspace():
            self._next()

    def next_int(self):
        self.skip_ws()
        p = self._pos
        while self.cur.isdigit():
            self._next()
        return int(self._line[p:self._pos])

    def skip_int(self):
        self.next_int()

    def next_line(self):
        if self._pos != 0:
            self._next_line()
        self._pos = self._len
        return self._line.rstrip()

    def check_eof(self):
        return self._line[self._pos:].isspace() and not self._source.read()


@contextmanager
def reader(filename, output=False):
    with open(filename) as source:
        reader = Reader(source, output)
        yield reader
        if output:
            reader.check_eof()


def ok(message=None):
    return Result.VERDICT_ACCEPTED, message if message else "Ok"


def failed(message=None):
    return Result.VERDICT_WRONG_ANSWER, message if message else "Wrong answer"


def check(out, ans, pos=0):
    if out != ans:
        message = 'output  : {}\n' \
                  'expected: {}'.format(out, ans)
        if pos > 0:
            message += '\n(#{})'.format(pos)
        raise WrongAnswerError(message)


def read_lines(outf, ansf, n=0):
    i = 1
    ans = ansf.next_line()
    while (i <= n or n == 0) and ans:
        out = outf.next_line()
        yield out, ans, i
        i += 1
        ans = ansf.next_line()
    if n > 0 and i <= n:
        raise Exception('There is no more lines in the answer (read: {}, required: {})'.format(i, n))


def read_ints(outf, ansf, n):
    for i in range(n):
        out = outf.next_int()
        ans = ansf.next_int()
        yield out, ans, i + 1