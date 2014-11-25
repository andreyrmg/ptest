from contextlib import contextmanager
import os

__author__ = 'andrey'


def read_begin(filename):
    with open(filename) as f:
        data = f.read(128)
        if f.read(1):
            data += '...'
        return data


@contextmanager
def lock_file(filename):
    while True:
        try:
            fd = os.open(filename, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError:
            import time
            time.sleep(1)
            continue
        try:
            yield
        finally:
            os.close(fd)
            os.unlink(filename)
        return
