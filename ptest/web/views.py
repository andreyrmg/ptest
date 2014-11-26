from datetime import datetime
from flask import render_template, request, session, abort, redirect, url_for, \
    flash

__author__ = 'Andrey'

from . import app, contest


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = contest.user(request.form['user_id'])
        if not user:
            flash(('error', 'error:', 'invalid user ID'))
        elif user.pwd != request.form['password']:
            flash(('error', 'error:', 'invalid password'))
        else:
            session['user'] = user.id
            flash(('success', '', 'Hello, ' + user.name + '!'))
            return redirect(url_for('problems'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    user_id = session.get('user')
    if user_id:
        session.pop('user', None)
        user = contest.user(user_id)
        flash(('notice', '',
               'Goodbye' + (', ' + user.name if user else '') + '!'))
    return redirect(url_for('problems'))


@app.route('/')
@app.route('/problems')
def problems():
    probs = contest.problems
    return render_template('problems.html', title='Problems', probs=probs)


@app.route('/submissions')
def submissions():
    if not session.get('user'):
        return redirect(url_for('login'))
    subs = contest.state['submissions']

    def subs_filter(sub):
        return (not request.args['user'] or sub.user == request.args['user']) and \
               (not request.args['prob'] or sub.prob == request.args['prob'])

    return render_template('submission-list.html',
                           title='Submissions', submissions=subs,
                           subs_filter=subs_filter)


@app.route('/submission/<sub_id>')
def submission(sub_id):
    if not session.get('user'):
        return abort(404)
    sub_and_result = contest.state['submissions'].get(sub_id)
    if not sub_and_result:
        abort(404)
    sub, result = sub_and_result
    if session['user'] != 'admin' and session['user'] != sub.user and \
            not contest.finished:
        abort(404)
    source = contest.source(sub)
    return render_template('submission.html', title='Submission ' + sub_id,
                           submission=sub, result=result, source=source)


@app.route('/standings')
def standings():
    s = contest.state['standings']
    return render_template('standings.html', title='Standings',
                           standings=s)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    t = datetime.now()
    status = contest.status(t)
    if not status:
        flash(('notice', '', 'Contest has not yet begun!'))
        return redirect(url_for('problems'))
    if status == 'finish':
        flash(('notice', '', 'Contest has finished!'))
        return redirect(url_for('standings'))
    if not session.get('user'):
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST':
        source = request.files['source']
        if not request.form['prob']:
            flash(('error', 'error:', 'choose problem'))
        elif not request.form['lang']:
            flash(('error', 'error:', 'choose language'))
        elif not source:
            flash(('error', 'error:', 'choose source file'))
        else:
            user = session['user']
            prob = request.form['prob']
            lang = request.form['lang']
            contest.submit(user, prob, lang, source.filename, source.stream)
            flash(('success', 'success:', 'solution sent!'))
            return redirect(url_for('submissions', user=user))
    return render_template('submit.html', title='Submit', error=error)