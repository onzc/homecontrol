__author__ = 'Andy'
# all the imports
import os
import sqlite3
import random
import datetime
import user
import userfactory
import roomfactory
import roomgroupfactory
import devicefactory
import devicegroupfactory

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


def init_defaultdata():
    with app.app_context():
        db = get_db()
        with app.open_resource('defaultdata.sql', mode='r') as f:
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


@app.route('/home')
@app.route('/')
def show_home():
    init_db()
    init_defaultdata()
    init_testdata()
    db = get_db()
    rf = roomfactory.RoomFactory()
    rooms = rf.get_rooms(db)
    lin = None
    if 'currentuserid' in session:
        lin = session['currentuserid']
    else:
        lin = False
    if lin == True:
        uf = userfactory.Userfactory()
        user = uf.getuser(db, session['currentuserid'])
        return render_template('home.html', rooms=rooms, user=user)
    else:
        return render_template('home.html', rooms=rooms, user=None)


def device_list():
    if isloggedin() == True:
        uf = userfactory.Userfactory()
        db = get_db()
        user = uf.getuser(db, session['currentuserid'])
        df = devicefactory.DeviceFactory()
        devices = df.get_devices(db)
        return render_template('devicelist.html', user=user, devices=devices)
    else:
        error = 'Not authorised'
        return render_template('home.html', error=error)


def room_list():
    if isloggedin() == True:
        uf = userfactory.Userfactory()
        db = get_db()
        user = uf.getuser(db, session['currentuserid'])
        rf = roomfactory.RoomFactory()
        rooms = rf.get_rooms(db)
        return render_template('roomlist.html', user=user, rooms=rooms)
    else:
        error = 'Not authorised'
        return render_template('home.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        uf = userfactory.Userfactory()
        userid = uf.validuser(db, request.form['username'], request.form['password'])
        if userid > 0:
            user = uf.getuser(db, userid)
            session['currentuserid'] = userid
            session['logged_in'] = True
            flash('Logged in ' + user.first + ' ' + user.last)
            return redirect(getjqm_url('show_home'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    userid = session['currentuserid']
    uf = userfactory.Userfactory()
    db = get_db()
    user = uf.getuser(db, userid)
    session.pop('logged_in', None)
    session.pop('currentuserid', None)
    flash('Logged out ' + user.first + ' ' + user.last)
    return redirect(getjqm_url('show_home'))


@app.route('/getuser', methods=['GET'])
def getuser():
    db = get_db()
    uf = userfactory.Userfactory()
    userid = int(request.args.get('userid'))
    userdetails = uf.getuser(db, userid)
    return render_template('userdetails.html', userdetails=userdetails)


@app.route('/list/<item>')
def list(item):
    if isloggedin() == True:
        db = get_db()
        uf = userfactory.Userfactory()
        user = uf.getuser(db, session['currentuserid'])
        item = item.lower()
        if item == 'room':
            return room_list()
        elif item == 'roomgroup':
            pass
        elif item == 'device':
            return device_list()
        elif item == 'user':
            pass
    else:
        error = 'Not authorised'
        return render_template('home.html', error=error)


@app.route('/edit/<item>/<id>')
def edit(item, id):
    if isloggedin() == True:
        db = get_db()
        uf = userfactory.Userfactory()
        user = uf.getuser(db, session['currentuserid'])
        item = item.lower()
        if item == 'room':
            rgf = roomgroupfactory.Roomgroupfactory()
            roomgroups = rgf.getroomgroups(db)
            rf = roomfactory.RoomFactory()
            room = rf.get_room(db, id)
            return render_template('addroom.html', user=user, roomgroups=roomgroups, room=room)
        elif item == 'roomgroup':
            pass
        elif item == 'device':
            dgf = devicegroupfactory.DeviceGroupFactory()
            devicegroups = dgf.get_devicegroups(db)
            df = devicefactory.DeviceFactory()
            device = df.get_device(db, id)
            return render_template('addeditdevice.html', user=user, devicegroups=devicegroups, device=device)
        elif item == 'user':
            pass
    else:
        error = 'Not authorised'
        return render_template('home.html', error=error)


@app.route('/add/<item>')
def add(item):
    if isloggedin() == True:
        db = get_db()
        uf = userfactory.Userfactory()
        user = uf.getuser(db, session['currentuserid'])
        item = item.lower()
        if item == 'room':
            rgf = roomgroupfactory.Roomgroupfactory()
            roomgroups = rgf.getroomgroups(db)

            return render_template('addroom.html', user=user, roomgroups=roomgroups, room=None)
        elif item == 'roomgroup':
            pass
        elif item == 'device':
            dgf = devicegroupfactory.DeviceGroupFactory()
            devicegroups = dgf.get_devicegroups(db)
            df = devicefactory.DeviceFactory()
            return render_template('addeditdevice.html', user=user, devicegroups=devicegroups, device=None)
        elif item == 'user':
            pass
    else:
        error = 'Not authorised'
        return render_template('home.html', error=error)


@app.route('/delete/<item>/<id>')
def delete(item, id):
    if isloggedin() == True:
        db = get_db()
        item = item.lower()
        if item == 'room':
            rf = roomfactory.RoomFactory()
            rf.delete_room(db, id)
            return room_list()
        elif item == 'roomgroup':
            pass
        elif item == 'device':
            df = devicefactory.DeviceFactory()
            df.delete(db, id)
            return device_list()
        elif item == 'user':
            pass
    else:
        error = 'Not authorised'
        return render_template('home.html', error=error)


@app.route('/link/<item>/<id1>/<id2>')
def link(item, id1, id2):
    if isloggedin() == True:
        db = get_db()
        item = item.lower()
        rf = roomfactory.RoomFactory()

        if item == 'roomdevice':
            room = rf.get_room(db, id1)
            df = devicefactory.DeviceFactory()
            device = df.get_device(db, id2)
            room.add_device(db, device)
            return edit('room', id1)

        else:
            error = 'Not authorised'
            return render_template('home.html', error=error)


@app.route('/unlink/<item>/<id1>/<id2>')
def unlink(item, id1, id2):
    if isloggedin() == True:
        db = get_db()
        item = item.lower()
        rf = roomfactory.RoomFactory()

        if item == 'roomdevice':
            room = rf.get_room(db, id1)
            df = devicefactory.DeviceFactory()
            device = df.get_device(db, id2)
            room.remove_device(db, device)
            return edit('room', id1)

        else:
            error = 'Not authorised'
            return render_template('home.html', error=error)


@app.route('/device/<action>/<deviceid>')
def device_action(action, deviceid):
    if isloggedin() == True:
        db = get_db()
        action = action.lower()
        df = devicefactory.DeviceFactory()
        device = df.get_device(db, deviceid)
        if action == 'pair':
            device.pair(db)
        elif action == 'unpair':
            device.unpair(db)
        elif action == 'on':
            device.on()
        elif action == 'off':
            device.off()
        return edit('device', deviceid)
    else:
        error = 'Not authorised'
        return render_template('home.html', error=error)


@app.route('/save/<item>', methods=['POST'])
def save(item):
    if isloggedin() == True:
        db = get_db()
        item = item.lower()
        if item == 'room':
            return save_room(db)
        elif item == 'roomgroup':
            pass
        elif item == 'device':
            return save_device(db)
        elif item == 'user':
            pass
    else:
        error = 'Not authorised'
        return render_template('home.html', error=error)


def save_device(db):
    if 'save' in request.form:
        devicename = request.form['name']
        devicegroups = []
        deviceid = request.form['deviceid']
        address = request.form['address']
        subid = request.form['subid']
        devicetype = request.form['devicetype']
        paired = 0
        for f in request.form:
            if f.startswith('checkbox_'):
                devicegroupid = f.replace('checkbox_', '')
                devicegroups.append(int(devicegroupid))

        # need to check we have at least 1 group here
        df = devicefactory.DeviceFactory()
        if deviceid == '':
            deviceid = df.create(db, devicename, address, subid, devicetype, paired, devicegroups)
        else:
            df.update(db, deviceid, devicename, address, subid, devicetype, paired, devicegroups)

        return edit('device', deviceid)
    else:
        return device_list()


def save_room(db):
    if 'save' in request.form:
        roomname = request.form['name']
        roomgroups = []
        roomid = request.form['roomid']
        for f in request.form:
            if f.startswith('checkbox_'):
                roomgroupid = f.replace('checkbox_', '')
                roomgroups.append(int(roomgroupid))

        # need to check we have at least 1 room group here
        rf = roomfactory.RoomFactory()
        if roomid == '':
            rf.create_room(db, roomname, roomgroups)
        else:
            rf.update_room(db, roomid, roomname, roomgroups)

    return room_list()


@app.route('/getroom', methods=['GET'])
def getroom():
    db = get_db()
    rf = roomfactory.RoomFactory()
    roomid = int(request.args.get('roomid'))
    roomdetails = rf.get_room(db, roomid)
    lin = None
    if 'currentuserid' in session:
        lin = session['currentuserid']
    else:
        lin = False

    if lin == True:
        uf = userfactory.Userfactory()
        db = get_db()
        user = uf.getuser(db, session['currentuserid'])
        return render_template('roomdetails.html', user=user, room=roomdetails)
    else:
        error = 'Not authorised'
    return render_template('home.html', error=error)


@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        usergroup = request.form['usergroup']
        db = get_db()
        uf = userfactory.Userfactory()
        uf.createuser(db, username, password, firstname, lastname, usergroup)

    return render_template('login.html', error=error)


@app.context_processor
def utility_processor():
    def jqm_url(method):
        return getjqm_url(method)

    return dict(jqm_url=jqm_url)


def getjqm_url(method):
    r = url_for(method)
    r = r + '?l=' + str(random.random())
    return r


def isloggedin():
    lin = None
    if 'currentuserid' in session:
        lin = True
    else:
        lin = False
    return lin


if __name__ == '__main__':
    app.run()
