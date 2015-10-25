import os
from subprocess import CalledProcessError, check_call, STDOUT, TimeoutExpired
import time


class RuntimeError(Exception):
    def __init__(self, time, exitcode):
        self.time = time
        self.exitcode = exitcode


class TimeoutExpiredError(Exception):
    def __init__(self, time):
        self.time = time


def run(cmd, workdir, infname, outfname, timeout):
    with open(infname) as inf, open(outfname, 'w') as outf:
        start_time = time.time()
        try:
            check_call(cmd, stdin=inf, stdout=outf, stderr=STDOUT,
                       cwd=workdir, timeout=timeout / 1000)
            end_time = time.time()
            return end_time - start_time
        except CalledProcessError as e:
            end_time = time.time()
            raise RuntimeError(end_time - start_time, e.returncode)
        except TimeoutExpired as e:
            end_time = time.time()
            raise TimeoutExpiredError(end_time - start_time)


if os.name == 'nt':
    import ptest.process_nt as process_nt
    def run_nt(cmd, workdir, infname, outfname, timeout):
        try:
            rawcmd = ' '.join(cmd)
            return process_nt.run(rawcmd, workdir, infname, outfname, timeout)
        except process_nt.ProcessRuntimeError as e:
            raise RuntimeError(*e.args)
        except process_nt.ProcessTimeoutExpired as e:
            raise TimeoutExpiredError(*e.args)
    run = run_nt
