__author__ = 'Andy'
import os
import homecontrol
import user
import unittest
import tempfile
import user
import userfactory

class homecontrolTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, homecontrol.app.config['DATABASE'] = tempfile.mkstemp()
        homecontrol.app.config['TESTING'] = True
        self.app = homecontrol.app.test_client()
        homecontrol.init_db()
        homecontrol.init_testdata()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(homecontrol.app.config['DATABASE'])


    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Unbelievable.' in rv.data


    def test_login_logout(self):
        rv = self.login('1', 'p')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'p')
        assert 'Invalid username' in rv.data
        rv = self.login('1', 'defaultx')
        assert 'Invalid password' in rv.data


    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    def getuser(self, userid):
        return self.app.get('/getuser', query_string = 'userid=' + str(userid), follow_redirects=True)

    def adduser(self, username, password, firstname, lastname, usergroup):
        return self.app.post('/adduser', data=dict(username=username, password=password, firstname=firstname, lastname=lastname, usergroup=usergroup),follow_redirects=True)


    def testgetuser(self):
        self.testadduser()
        rv = self.getuser(1)
        assert 'User Details' in rv.data

    def testadduser(self):
        rv = self.adduser('test','house','f','L', 1)
        assert  rv

if __name__ == '__main__':
    unittest.main()
