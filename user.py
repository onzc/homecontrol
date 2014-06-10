class User:
    _userid = 0
    _username = ''
    _password = ''
    _first = ''
    _last = ''
    _usergroupid = ''
    def __init__(self, userid, username, password, first, last, usergroupid):
        self._userid= userid
        self._username = username
        self._password = password
        self._first = first
        self._last = last
        self._usergroupid = usergroupid


