__author__ = 'Andy'
import os
import homecontrol
import unittest
import tempfile

class homecontrolTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, homecontrol.app.config['DATABASE'] = tempfile.mkstemp()
        homecontrol.app.config['TESTING'] = True
        self.app = homecontrol.app.test_client()
        homecontrol.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(homecontrol.app.config['DATABASE'])


    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Unbelievable.' in rv.data

    def test_loadtestData(self):
        homecontrol.init_testdata()
        rv = self.app.get('/')
        assert 'Unbelievable.' not in rv.data

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


if __name__ == '__main__':
    unittest.main()
