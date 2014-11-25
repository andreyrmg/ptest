import argparse
import os
import re
from ptest.contest import Contest

__author__ = 'Andrey'

parser = argparse.ArgumentParser('Submit solutions')
parser.add_argument('solutions_dir', metavar='DIR', help='directory with solutions')
parser.add_argument('-c', default='.', help='contest directory')
parser.add_argument('-p', default='(?P<classroom>\d+)_(?P<number>\d+)(?P<prob>[a-z])\.(pas|dpr)',
                    help='solution name pattern')

args = parser.parse_args()

contest = Contest(args.c)

p = re.compile(args.p, re.IGNORECASE)
for root, _, files in os.walk(args.solutions_dir):
    for name in files:
        m = re.fullmatch(p, name)
        if not m:
            continue
        upper_name = name.upper()
        _, ext = os.path.splitext(upper_name)
        if ext == '.PAS':
            lang = 'Free Pascal'
        elif ext == '.DPR':
            lang = 'Delphi'
        else:
            print('cannot determinate language for', name)
            continue
        user = '{:03d}-{:02d}'.format(int(m.group('classroom')), int(m.group('number')))
        prob = m.group('prob').upper()
        print('submit', 'user:', user, 'lang:', lang, 'prob:', prob, os.path.join(root, name))
        contest.submit(user, prob, lang, os.path.join(root, name))
