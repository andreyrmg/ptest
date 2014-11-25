import os
import csv
import random
import re
import string

LETTERS_DIGITS = string.ascii_letters + string.digits

__author__ = 'Andrey'


def next_pwd(n=5):
    pwd_gen = (random.choice(LETTERS_DIGITS) for _ in range(n))
    return ''.join(pwd_gen)


def extract_info(filename):
    n = None
    s = None
    k = None
    with open(filename) as f:
        for line in f.readlines():
            i = line.find('@name:')
            if i > -1:
                n = line[i+6:].strip()
            i = line.find('@school:')
            if i > -1:
                s = line[i+8:].strip()
            i = line.find('@class:')
            if i > -1:
                k = line[i+7:].strip()
    return n, s, k


existing_users = set()

if os.path.isfile('users.csv'):
    with open('users.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            existing_users.add(row[0])


p = re.compile(r'(?P<classroom>\d+)_(?P<number>\d+).*')

users = []
for root, _, files in os.walk(r'c:\Users\Andrey\Downloads\olymp-2013\src'):
    for name in files:
        m = p.fullmatch(name)
        if not m:
            continue
        classroom = int(m.group('classroom'))
        number = int(m.group('number'))
        name, school, klass = extract_info(os.path.join(root, name))
        user_id = '{:03d}-{:02d}'.format(classroom, number)
        if user_id in existing_users:
            continue
        row = (
            user_id,
            name, school, klass,
            next_pwd()
        )
        users.append(row)
        existing_users.add(user_id)

with open('users.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(users)