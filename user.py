class User:
    userid = 0
    username = ''
    password = ''
    first = ''
    last = ''
    usergroupid = ''
    def __init__(self, userid, username, password, first, last, usergroupid):
        self.userid= userid
        self.username = username
        self.password = password
        self.first = first
        self.last = last
        self.usergroupid = usergroupid


