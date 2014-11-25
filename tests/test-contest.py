import csv
from datetime import datetime
import os
from pprint import pprint
import shutil
import time
from ptest import language, problem
from ptest.contest import Contest
from ptest.util import lock_file

__author__ = 'Andrey'

import unittest


class ContestTestCase(unittest.TestCase):

    def setUp(self):
        if os.path.isdir('./contest/submits'):
            shutil.rmtree('./contest/submits')
        self.contest = Contest('./contest')

    def test_submits_directory_exists(self):
        self.assertTrue(os.path.isdir(self.contest.submit_dir))

    def test_submit_solution(self):
        self.contest.submit('510-06', 'A', 'Delphi', './sources/510_06A.dpr')
        self.assertEqual(1, len(self.contest.submissions()))
        self.contest.submit('515-05', 'A', 'Free Pascal', './sources/515_05A.pas')
        self.assertEqual(2, len(self.contest.submissions()))


if __name__ == '__main__':
    unittest.main()
