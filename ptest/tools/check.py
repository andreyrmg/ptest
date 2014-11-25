import argparse
import msvcrt
import sys
from collections import defaultdict
from ptest.contest import Contest
from ptest.result import Result

__author__ = 'Andrey'

parser = argparse.ArgumentParser('Submit solutions')
parser.add_argument('ids', metavar='ID', type=str, nargs='*',
                    help='submission identifiers')
parser.add_argument('-c', default='.', help='contest directory')
parser.add_argument('-p', '--pretest', dest='pretest', action='store_true')
parser.add_argument('--system', dest='system', action='store_true')
parser.add_argument('-s', '--store', dest='store', action='store_true')
parser.add_argument('-f', '--force', dest='force', action='store_true')
parser.add_argument('--pause', dest='pause', action='store_true')
parser.set_defaults(pretest=False, system=False, store=False, force=False,
                    pause=False)

args = parser.parse_args()

contest = Contest(args.c)


def check_and_print_result(submission, pretest=False, store=False):
    result = contest.check_submission(submission, pretest=pretest, store=store)

    points = 0
    for t, r in result.tests.items():
        print('test #{}: {}, time: {:.3f} s'.format(t, r.verdict, r.time))
        print(r.details)
        print()
        if r.verdict == Result.VERDICT_ACCEPTED:
            points += 1
        if r.verdict == Result.VERDICT_INTERNAL_ERROR:
            sys.exit('Ooops!!!')

    print('=' * 25)
    print(submission)
    print('verdict:', result.verdict, result.details)
    print('total:', points)
    print('=' * 25)
    print()


def maybe_pause():
    if args.pause:
        print('press any key to continue...')
        msvcrt.getch()


if __name__ == '__main__':
    if args.ids:
        for sub in contest.submissions():
            if sub.id not in args.ids:
                continue
            check_and_print_result(sub, store=args.store)
            maybe_pause()
        sys.exit()
    if args.pretest:
        for sub in contest.submissions()[::-1]:
            if contest.need_check(sub):
                check_and_print_result(sub, pretest=True, store=args.store)
            maybe_pause()
        sys.exit()
    if args.system:
        users = defaultdict(set)
        subs = []
        for sub in contest.submissions():
            probs = users[sub.user]
            if sub.prob in probs:
                continue
            subs.append(sub)
            probs.add(sub.prob)
        print('{} submission(s) for testing'.format(len(subs)))
        for sub in subs[::-1]:
            check_and_print_result(sub, pretest=False, store=args.store)
            maybe_pause()
        sys.exit()
