import os
import unittest

from ptest import language, problem
from ptest.result import Result


__author__ = 'andrey'


class ProblemTestCase(unittest.TestCase):
    def setUp(self):
        problems = problem.load_from_file('./contest/problem.ini')
        self.problem = problems['A']

        compilers = language.load_from_file('./contest/compiler-{}.ini'.format(os.name))
        self.fpc = compilers['Free Pascal']
        self.dcc32 = compilers['Delphi']

    def test_finding_tests(self):
        self.assertEqual(15, self.problem.test_count)

    def test_check_500_03_A_pas(self):
        result = self.problem.check('./sources/500_03A.pas', self.fpc)
        self.assertEqual(Result.VERDICT_RUNTIME_ERROR, result.verdict)
        self.assertEqual('01', result.details)
        self.assertEqual('exit status: 2', result.at('01').details)

    def test_check_507_04_A_pas(self):
        result = self.problem.check('./sources/507_04A.pas', self.fpc)
        self.assertEqual(Result.VERDICT_TIMEOUT, result.verdict)
        self.assertEqual('01', result.details)
        self.assertEqual(Result.VERDICT_WRONG_ANSWER, result.at('03').verdict)

    def test_check_510_04_A_dpr(self):
        result = self.problem.check('./sources/510_04A.dpr', self.dcc32)
        self.assertEqual(Result.VERDICT_WRONG_ANSWER, result.verdict)
        self.assertEqual('03', result.details)
        self.assertEqual(Result.VERDICT_RUNTIME_ERROR, result.at('04').verdict)
        self.assertEqual('exit status: 1', result.at('04').details)

    def test_check_510_06_A_dpr(self):
        result = self.problem.check('./sources/510_06A.dpr', self.dcc32)
        self.assertEqual(Result.VERDICT_ACCEPTED, result.verdict)

    def test_check_515_05_A_pas(self):
        result = self.problem.check('./sources/515_05A.pas', self.fpc)
        self.assertEqual(Result.VERDICT_PRESENTATION_ERROR, result.verdict)
        self.assertEqual('01', result.details)

    def test_check_515_11_A_pas(self):
        result = self.problem.check('./sources/515_11A.pas', self.fpc)
        self.assertEqual(Result.VERDICT_WRONG_ANSWER, result.verdict)
        self.assertEqual('11', result.details)
        self.assertEqual('output  : 19 29\n'
                         'expected: 6 112\n'
                         '(#7)',
                         result.at('11').details)


if __name__ == '__main__':
    unittest.main()
