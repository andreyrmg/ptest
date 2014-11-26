from datetime import datetime
from flask import Flask
from ptest.contest import Contest

__author__ = 'Andrey'


app = Flask(__name__)
app.config.from_object('config')

contest = Contest('.',
                  admin_pwd=app.config.get('ADMIN_PASSWORD'),
                  start=app.config.get('CONTEST_START'),
                  duration=app.config.get('CONTEST_DURATION'))

app.jinja_env.globals['contest'] = contest
app.jinja_env.globals['now'] = datetime.now

from . import views