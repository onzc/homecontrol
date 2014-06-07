__author__ = 'Andy'
# all the imports
import os
import sqlite3
import random
import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'homecontrol.db'),
    DEBUG=True,
    SECRET_KEY='oweicfoiwfiojewf8u839cmmckmoiIJSJDijidjdajmxm',
    USERNAME='1',
    PASSWORD='p'
))
app.config.from_envvar('HOMECONTROL_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def init_testdata():
    with app.app_context():
        db = get_db()
        with app.open_resource('testdata.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_home():
    db = get_db()
    cur = db.execute('select room_id, name from rooms order by room_id asc')
    rooms = cur.fetchall()
    return render_template('home.html', rooms=rooms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(getjqm_url('show_home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(getjqm_url('show_home'))


@app.context_processor
def utility_processor():
    def jqm_url(method):
        return getjqm_url(method)

    return dict(jqm_url=jqm_url)


def send_url(method):

    response = app.make_response(url_for(method))

    response.headers.add('Last-Modified', datetime.datetime.now())
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    response.headers.add('Pragma', 'no-cache')

    return response


def getjqm_url(method):
    r = url_for(method)
    r = r + '?l=' + str( random.random())
    return r


if __name__ == '__main__':
    app.run()
