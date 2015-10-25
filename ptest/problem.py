from collections import OrderedDict
from configparser import ConfigParser
import importlib.machinery
import os
import re
import shutil
import traceback
from ptest.checklib import reader, WrongAnswerError, PresentationError
from ptest.language import CompilationError
from ptest.process import run, RuntimeError, TimeoutExpiredError
from ptest.result import Result, TestResult, compilation_error, unknown_error

__author__ = 'andrey'


class Problem(object):
    def __init__(self, id, title, test_dir, input_regex=r'(?P<test>\d+)',
                 answer_name='<test>.out', input_name='input.txt',
                 output_name='output.txt', timeout=1050, checker=None,
                 pretests=None):
        self._warnings = []
        self._id = id
        self._title = title
        self._test_dir = os.path.abspath(test_dir)
        self._input_regex = re.compile(input_regex)
        self._answer_name = answer_name
        self._input_name = input_name
        self._output_name = output_name
        self._timeout = timeout
        self._find_tests(set(pretests.split(',') if pretests else []))
        self._load_checker(checker)

    def _find_tests(self, pretests):
        self._tests = []
        self._pretests = []
        for root, _, files in os.walk(self._test_dir):
            for name in files:
                m = self._input_regex.fullmatch(name)
                if not m: continue
                test_name = m.group('test')
                answer_name = self._answer_name.replace('<test>',
                                                        test_name)
                if answer_name not in files:
                    self._warning("no answer file for the test '{}': {}"
                                  .format(name, answer_name))
                self._tests.append((name, answer_name))
                if test_name in pretests:
                    self._pretests.append((name, answer_name))
                    pretests.remove(test_name)
        if pretests:
            self._warning('some pretests not found: {}'.format(pretests))

    def _load_checker(self, checker):
        if not checker:
            return self._warning('no check')
        if not os.path.isabs(checker):
            checker = os.path.join(self._test_dir, checker)
        fn = os.path.abspath(checker)
        module_name = 'check_{:08x}'.format(abs(hash(fn)))
        self._checker = importlib.machinery.SourceFileLoader(module_name, fn).load_module()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def input_name(self):
        return self._input_name

    @property
    def output_name(self):
        return self._output_name

    @property
    def timeout(self):
        round_timeout = self._timeout // 100 * 100
        if round_timeout < 1000:
            return '{:d} ms'.format(round_timeout)
        else:
            return '{:d} s'.format(round_timeout // 1000)

    @property
    def test_count(self):
        return len(self._tests)

    def _warning(self, warning):
        self._warnings.append(warning)

    def check(self, source_filename, language, pretest=False):
        try:
            return self._check(source_filename, language, pretest)
        except CompilationError as e:
            return compilation_error(self, language, e)
        except Exception:
            return unknown_error(self, language)

    def _check(self, source_filename, language, pretest):
        fullname = os.path.abspath(source_filename)
        if not os.path.isfile(fullname):
            raise Exception("file '{}' not exists".format(fullname))
        if not language:
            raise Exception("language not specified")

        result = Result(self._id, language.name, pretest)

        import tempfile

        with tempfile.TemporaryDirectory('p-test') as working_dir:
            run_cmd = language.prepare(working_dir, fullname)
            tests = self._pretests if pretest else self._tests
            for test, answer in tests:
                test_fn = os.path.join(self._test_dir, test)
                answer_fn = os.path.join(self._test_dir, answer)
                test_result = self._run_test(working_dir, run_cmd,
                                             test_fn, answer_fn)
                result.add_test_result(test, test_result)
        return result

    def _run_test(self, working_dir, cmd, test_fn, answer_fn):
        input_fn = os.path.join(working_dir, self._input_name)
        output_fn = os.path.join(working_dir, self._output_name)
        try:
            shutil.copyfile(test_fn, input_fn)
            # open(output_fn, 'a')
            try:
                time = run(cmd, working_dir, input_fn, output_fn, self._timeout)
                # time = run(cmd[0], working_dir, input_fn, output_fn, self._timeout)
                verdict, details = self._run_checker(test_fn, output_fn, answer_fn)
            except RuntimeError as e:
                time = e.time
                verdict = Result.VERDICT_RUNTIME_ERROR
                details = 'exit status: {}'.format(e.exitcode)
            except TimeoutExpiredError as e:
                time = e.time
                verdict = Result.VERDICT_TIMEOUT
                details = None
            return TestResult(verdict, details, time, test_fn, output_fn, answer_fn)
        finally:
            os.unlink(input_fn)
            os.unlink(output_fn)

    def _run_checker(self, test_fn, output_fn, answer_fn):
        if not self._checker:
            return Result.VERDICT_INTERNAL_ERROR, 'checker not specified'
        try:
            with reader(test_fn) as i, reader(output_fn, output=True) as o, reader(answer_fn) as a:
                result = self._checker.run(i, o, a)
                if not isinstance(result, tuple) or len(result) != 2:
                    return Result.VERDICT_INTERNAL_ERROR, 'checker failed: bad result ' + repr(result)
                return result
        except WrongAnswerError as e:
            return Result.VERDICT_WRONG_ANSWER, str(e)
        except PresentationError as e:
            return Result.VERDICT_PRESENTATION_ERROR, str(e)
        except Exception:
            return Result.VERDICT_INTERNAL_ERROR, 'checker failed: ' + traceback.format_exc()


def load_from_config(config):
    return OrderedDict(
        (prob_id, Problem(prob_id, **config[prob_id]))
        for prob_id in config.sections()
    )


def load_from_file(filename):
    cwd = os.getcwd()
    try:
        fn = os.path.abspath(filename)
        dir, _ = os.path.split(fn)
        os.chdir(dir)
        config = ConfigParser()
        config.read(fn, encoding='utf-8')
        return load_from_config(config)
    finally:
        os.chdir(cwd)
