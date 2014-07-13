__author__ = 'Andy'
import os
import homecontrol
import user
import unittest
import tempfile
import user
import userfactory
import serial
import devicefactory
import time
import serialControl
from flask import Flask, url_for

class homecontrolTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, homecontrol.app.config['DATABASE'] = tempfile.mkstemp()
        # self.db_fd, homecontrol.app.config['DATABASE'] = 'C:/Users/Andy/Documents/pythonprojects/homecontrolTest'
        self.app = homecontrol.app.test_client()
        homecontrol.init_db()
        homecontrol.init_testdata()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(homecontrol.app.config['DATABASE'])

    def testHome(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        assert 'stair' in rv.data


    def test_login_logout(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.logout()
        assert 'Logged out' in rv.data
        rv = self.login('adminx', 'p')
        assert 'Invalid username or password' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid username or password' in rv.data


    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    def getuser(self, userid):
        return self.app.get('/getuser', query_string = 'userid=' + str(userid), follow_redirects=True)


    def getroom(self, roomid):
        return self.app.get('/getroom', query_string='roomid=' + str(roomid), follow_redirects=True)


    def adduser(self, username, password, firstname, lastname, usergroup):
        return self.app.post('/adduser', data=dict(username=username, password=password, firstname=firstname, lastname=lastname, usergroup=usergroup),follow_redirects=True)

    def roomlist(self):
        return self.app.get('/list/room', follow_redirects=True)


    def devicelist(self):
        return self.app.get('/list/device', follow_redirects=True)


    def userlist(self):
        return self.app.get('/list/user', follow_redirects=True)

    def add_device(self, name, address, subid, devicetype, paired):
        return self.app.post('/save/device',
                             data=dict(name=name, checkbox_1='on', save='xx', deviceid='', address=address, subid=subid,
                                       devicetype=devicetype, paired=paired),
                             follow_redirects=True)

    def edit_device(self, deviceid, name, address, subid, devicetype, paired):
        return self.app.post('/save/device',
                             data=dict(name=name, checkbox_1='on', save='xx', deviceid=str(deviceid), address=address,
                                       subid=subid,
                                       devicetype=devicetype, paired=paired),
                             follow_redirects=True)

    def addroom(self, name):
        return self.app.post('/save/room', data=dict(name=name, checkbox_1='on', save='xx', roomid=''),
                             follow_redirects=True)


    def editroom(self, name, roomid):
        return self.app.post('/save/room', data=dict(name=name, checkbox_2='on', save='xx', roomid=str(roomid)),
                             follow_redirects=True)


    def delete(self, item, id):
        return self.app.get('/delete/' + item + '/' + str(id))


    def link_device_room(self, item, roomid, deviceid):
        return self.app.get('/link/' + item + '/' + str(roomid) + '/' + str(deviceid))


    def unlink_device_room(self, item, roomid, deviceid):
        return self.app.get('/unlink/' + item + '/' + str(roomid) + '/' + str(deviceid))

    def device_action(self, action, deviceid):
        return self.app.get('/device/' + action + '/' + str(deviceid))

    def testgetuser(self):
        self.testadduser()
        rv = self.getuser(1)
        assert 'User Details' in rv.data


    def testadduser(self):
        rv = self.adduser('test','house','f','L', 1)
        assert  rv


    def test_show_edit_device(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.app.get('edit/device/1')
        assert 'simple switch' in rv.data


    def test_create_device(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.add_device('test device', 1, 2, 'test type', 0)
        assert 'test device' in rv.data


    def test_update_device(self):
        deviceid = 1
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.edit_device(deviceid, 'edited device', 1, 2, 'edited type', 0)
        assert 'edited device' in rv.data


    def test_show_add_device(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.app.get('add/device')
        assert 'Add Device' in rv.data


    def testshowaddroom(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.app.get('/add/room')
        assert 'Add Room' in rv.data


    def testgetroom(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.getroom(1)
        assert 'Room Details' in rv.data


    def testcreateroom(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.addroom('test room')
        assert 'test room' in rv.data


    def testupdateroom(self):
        roomid = 1
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.editroom('edited room', roomid)
        assert 'edited room' in rv.data
        rv = self.app.get('/')
        assert 'stairs' in rv.data

    def testroomlist(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.roomlist()
        assert 'Kitchen' in rv.data


    def test_device_list(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.devicelist()
        assert 'simple switch' in rv.data


    def test_user_list(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.userlist()
        assert 'registered' in rv.data

    def test_delete_device(self):
        homecontrol.init_db()
        homecontrol.init_testdata()
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.delete('device', 1)
        assert 'simple switch' not in rv.data


    def testdeleteroom(self):
        homecontrol.init_db()
        homecontrol.init_testdata()

        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.delete('room', 2)
        assert 'Kitchen' not in rv.data
        assert 'Lounge' in rv.data


    def test_edit_room(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.app.get('edit/room/1')
        assert 'simple switch' in rv.data


    def test_auto_allocate(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.app.get('autoallocate')
        assert '"success": true' in rv.data

    def test_link_unlink_room_device(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.unlink_device_room('roomdevice', 1, 1)
        assert 'No devices allocated so far' in rv.data
        rv = self.link_device_room('roomdevice', 1, 1)
        assert 'simple switch' in rv.data


    def test_device_action_pair_unpair(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.device_action('pair', 1)
        assert rv.status_code == 200
        rv = self.device_action('unpair', 1)
        assert rv.status_code == 200
        rv = self.device_action('off', 1)
        assert rv.status_code == 200


    def test_device_action_on_off(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.device_action('on', 1)
        assert rv.status_code == 200
        time.sleep(2)
        rv = self.device_action('off', 1)
        assert rv.status_code == 200


    def test_device_pair(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.device_action('pair', 1)

    def test_serial_pair(self):
        pair = 'PAIR,10,0,0,0,1,0,3,7,2,10,13|'
        sc = serialControl.SerialControl()
        sc.send_single_message(pair)

    def test_serial_on(self):
        on = 'SEND,7,0,0,0,1,0,3,7,2,10,13|'
        off = 'SEND,7,0,0,0,0,0,3,7,2,10,13|'
        # self.send_serial(on)
        sc = serialControl.SerialControl()
        sc.send_single_message(on)

    def test_serial_off(self):
        on = 'SEND,7,0,0,0,1,0,3,7,2,10,13|'
        off = 'SEND,7,0,0,0,0,0,3,7,2,10,13|'

        sc = serialControl.SerialControl()
        sc.send_single_message(off)



if __name__ == '__main__':
    unittest.main()
