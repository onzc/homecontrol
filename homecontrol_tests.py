__author__ = 'Andy'
import os
import homecontrol
import user
import unittest
import tempfile
import user
import userfactory
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


    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Unbelievable.' in rv.data


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

    def showroomlist(self):
        return self.app.get('/showrooms', follow_redirects=True)


    def addroom(self, name):
        return self.app.post('/createroom', data=dict(name=name, checkbox_1='on', saveroom='xx'), follow_redirects=True)


    def delete(self, item, id):
        return self.app.get('/delete/' + item + '/' + str(id))

    def testgetuser(self):
        self.testadduser()
        rv = self.getuser(1)
        assert 'User Details' in rv.data


    def testadduser(self):
        rv = self.adduser('test','house','f','L', 1)
        assert  rv


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


    def testshowroomlist(self):
        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.showroomlist()
        assert 'Kitchen' in rv.data


    def testdeleteroom(self):
        homecontrol.init_db()
        homecontrol.init_testdata()

        rv = self.login('admin', 'p')
        assert 'Logged in' in rv.data
        rv = self.delete('room', 2)
        assert 'Kitchen' not in rv.data
        assert 'Lounge' in rv.data


if __name__ == '__main__':
    unittest.main()
