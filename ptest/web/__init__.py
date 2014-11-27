from datetime import datetime
import os
from flask import Flask
from ptest.contest import Contest

__author__ = 'Andrey'

cwd = os.path.abspath(os.getcwd())
app = Flask(__name__,
            instance_path=cwd,
            instance_relative_config=True)
contest = None


def run(host='0.0.0.0', port=None, config=None):
    config = config or 'ptest.web.config.Config'
    app.config.from_object(config)
    app.config.from_pyfile('contest.cfg')

    global contest
    contest = Contest(cwd,
                      admin_pwd=app.config.get('ADMIN_PASSWORD'),
                      start=app.config.get('CONTEST_START'),
                      duration=app.config.get('CONTEST_DURATION'))

    app.jinja_env.globals['contest'] = contest
    app.jinja_env.globals['now'] = datetime.now

    from . import views

    app.run(host=host, port=port, threaded=True)