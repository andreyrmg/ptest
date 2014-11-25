from collections import OrderedDict
import traceback
from ptest.util import read_begin

__author__ = 'andrey'


class Result(object):

    VERDICT_UNKNOWN = 'Unknown'
    VERDICT_COMPILATION_ERROR = 'Compilation error'
    VERDICT_RUNTIME_ERROR = 'Runtime error'
    VERDICT_INTERNAL_ERROR = 'Internal error'
    VERDICT_TIMEOUT = 'Time limit exceeded'
    VERDICT_ACCEPTED = 'Accepted'
    VERDICT_WRONG_ANSWER = 'Wrong answer'
    VERDICT_PRESENTATION_ERROR = 'Presentation error'

    def __init__(self, prob, lang, pretest=False):
        self.prob = prob
        self.lang = lang
        self.pretest = pretest
        self.verdict = Result.VERDICT_ACCEPTED
        self.details = None
        self.tests = OrderedDict()
        self.total = 0
        self.max_time = 0

    def add_test_result(self, test, test_result):
        self.tests[test] = test_result
        if test_result.verdict == Result.VERDICT_ACCEPTED:
            self.total += 1
            self.max_time = max(test_result.time, self.max_time)
        if self.verdict == Result.VERDICT_ACCEPTED:
            # self.max_time = max(self.max_time, test_result.time)
            if test_result.verdict != Result.VERDICT_ACCEPTED:
                self.verdict = test_result.verdict
                self.details = test

    def at(self, test):
        return self.tests[test]


class TestResult(object):
    def __init__(self, verdict, details, time, inf, outf, ansf):
        self.verdict = verdict
        self.details = details
        self.time = time
        self.input = read_begin(inf)
        self.output = read_begin(outf)
        self.answer = read_begin(ansf)

    def __str__(self, *args, **kwargs):
        return '{}, details: {}, time: {:.3f} s'.format(self.verdict, self.details, self.time)


def compilation_error(problem, language, error):
    result = Result(problem.id, language.name)
    result.verdict = Result.VERDICT_COMPILATION_ERROR
    result.details = str(error)
    return result


def unknown_error(problem, language):
    result = Result(problem.id, language.name)
    result.verdict = Result.VERDICT_INTERNAL_ERROR
    result.details = traceback.format_exc()
    return result
