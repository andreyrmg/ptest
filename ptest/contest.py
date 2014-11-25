from collections import OrderedDict
import csv
from datetime import datetime, timedelta
import os
import tempfile
import time
import shutil
import pickle

from ptest import language, problem
from ptest.result import Result
from ptest.util import lock_file


__author__ = 'Andrey'


class SubmitError(Exception): pass


class Submission(object):
    def __init__(self, row):
        self.id, self.time, self.user, self.prob, self.lang, self.name = row

    @property
    def datetime(self):
        return datetime.fromtimestamp(int(self.time))

    def __str__(self, *args, **kwargs):
        strtime = self.datetime.strftime('%c')
        return '{} {}, user: {}, problem: {}, language: {}'.format(self.id,
                                                                   strtime,
                                                                   self.user,
                                                                   self.prob,
                                                                   self.lang)


class User(object):
    def __init__(self, row):
        self.id, self.name, self.school, self.klass, self.pwd = row

    def __str__(self):
        return '{}, school {}, class {}'.format(self.name, self.school,
                                                self.klass)


class AdminUser(User):
    def __init__(self, pwd):
        super().__init__(('admin', 'Administrator', None, None, pwd))


class Contest(object):
    def __init__(self, contest_dir, admin_pwd='Admin', start=None,
                 duration=timedelta(hours=4)):
        self._lock_file = os.path.join(contest_dir, '.submit.lock')
        self._submit_dir = os.path.join(contest_dir, 'submits')
        self._submit_file = os.path.join(self.submit_dir, 'submits.csv')
        os.makedirs(self.submit_dir, exist_ok=True)
        self._languages = language.load_from_file(os.path.join(contest_dir,
                                                               'compiler.ini'))
        self._problems = problem.load_from_file(os.path.join(contest_dir,
                                                             'problem.ini'))
        self._users = self._load_users(os.path.join(contest_dir, 'users.csv'))
        self._users['admin'] = AdminUser(admin_pwd)

        if start is None:
            start = datetime.now()
        end = start + duration
        self._state = dict(
            _last_update=0,
            start=start,
            end=end,
            submissions=OrderedDict()
        )

    @staticmethod
    def _load_users(filename):
        def read_users():
            with open(filename, newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    yield User(row)

        return dict((user.id, user) for user in read_users())

    @property
    def submit_dir(self):
        return self._submit_dir

    @property
    def problems(self):
        return self._problems.items()

    @property
    def languages(self):
        return self._languages.items()

    @property
    def state(self):
        t = time.time()
        if t - self._state['_last_update'] > 15:
            self._actualize_state(self.submissions())
        return self._state

    @property
    def is_run(self):
        t = datetime.now()
        return self.status(t) == 'run'

    @property
    def finished(self):
        t = datetime.now()
        return self.status(t) == 'finish'

    def status(self, t):
        if t < self._state['start']:
            return None
        if t <= self._state['end']:
            return 'run'
        return 'finish'

    def _actualize_state(self, subs):
        t = datetime.now()
        self._state['status'] = self.status(t)
        subs_with_result = OrderedDict()
        for sub in subs:
            result = None
            result_fn = self._submission_result(sub)
            if os.path.isfile(result_fn):
                with open(result_fn, 'rb') as f:
                    result = pickle.load(f)
            subs_with_result[sub.id] = (sub, result)
        self._state['submissions'] = subs_with_result
        standings = {}
        for sub, result in subs_with_result.values():
            user_result = standings.get(sub.user, dict(total=0, prob={}))
            if sub.prob in user_result['prob']:
                continue
            standings[sub.user] = user_result
            if not result or result.pretest and self.status(t) == 'finish':
                user_result['prob'][sub.prob] = '?'
                continue
            if result.pretest and self.status(t) == 'run':
                if result.verdict == Result.VERDICT_ACCEPTED:
                    user_result['prob'][sub.prob] = '+'
                    user_result['total'] += result.total
                else:
                    user_result['prob'][sub.prob] = '-'
                continue
            user_result['prob'][sub.prob] = result.total
            user_result['total'] += result.total
        standings = list(standings.items())
        standings.sort(key=lambda x: (x[1]['total'], x[0]), reverse=True)
        self._state['standings'] = standings

    def _next_id(self):
        if not os.path.isfile(self._submit_file):
            id = 1
        else:
            with open(self._submit_file, newline='') as f:
                reader = csv.reader(f)
                id = sum(1 for _ in reader) + 1
        return '{:05d}'.format(id)

    def _check_parameters(self, lang, prob, user):
        if user not in self._users:
            raise SubmitError('user {} not found'.format(user))
        if prob not in self._problems:
            raise SubmitError('problem {} not found (problems: {})'.format(prob,
                                                                           ', '.join(
                                                                               self._problems.keys())))
        if lang not in self._languages:
            raise SubmitError(
                'language {} not found (languages: {})'.format(prob, ', '.join(
                    self._languages.keys())))

    def submit(self, user, prob, lang, filename, stream=None):
        submit_time = int(time.time())

        self._check_parameters(lang, prob, user)

        subs = self.submissions()
        with lock_file(self._lock_file):
            sub_id = '{:05d}'.format(len(subs) + 1)
            store_fn = os.path.join(self.submit_dir, sub_id)
            if not stream:
                shutil.copyfile(filename, store_fn)
            else:
                with open(store_fn, 'wb') as f:
                    f.write(stream.read())
            _, name = os.path.split(filename)
            row = [sub_id, submit_time, user, prob, lang, name]
            with open(self._submit_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
                for sub in subs:
                    writer.writerow((sub.id, sub.time, sub.user, sub.prob,
                                     sub.lang, sub.name))
            subs.insert(0, Submission(row))
            self._actualize_state(subs)

    def submissions(self):
        with lock_file(self._lock_file):
            result = []
            if os.path.isfile(self._submit_file):
                with open(self._submit_file, newline='') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        result.append(Submission(row))
            return result

    def user(self, user_id):
        return self._users.get(user_id)

    def problem(self, prob_id):
        return self._problems.get(prob_id)

    def _submission_source(self, submission):
        return os.path.join(self.submit_dir, submission.id)

    def _submission_result(self, submission):
        return os.path.join(self.submit_dir, submission.id + '.result')

    def need_check(self, submission):
        source_fn = self._submission_source(submission)
        if not os.path.isfile(source_fn):
            raise SubmitError('source not found for {}'.format(submission))
        result_fn = self._submission_result(submission)
        if not os.path.isfile(result_fn):
            return True
        return os.path.getmtime(source_fn) >= os.path.getmtime(result_fn)

    def check_submission(self, submission, pretest=False, store=False):
        self._check_parameters(submission.lang, submission.prob,
                               submission.user)

        with tempfile.TemporaryDirectory('p-test-source') as temp_dir:
            prob = self._problems[submission.prob]
            lang = self._languages[submission.lang]

            src = self._submission_source(submission)
            dst = os.path.join(temp_dir, submission.name)
            shutil.copyfile(src, dst)

            result = prob.check(dst, lang, pretest)

            if store:
                with open(self._submission_result(submission), 'wb') as f:
                    pickle.dump(result, f, protocol=pickle.DEFAULT_PROTOCOL)

            return result

    def source(self, sub):
        with open(self._submission_source(sub)) as source:
            return source.read()

