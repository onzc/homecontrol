import homecontrol
import user
import flask


class Userfactory():

    def getusers(self, db):
        cur = db.execute('select user_id from users')
        userrows = cur.fetchall()
        users = []
        for row in userrows:
            users.append(self.getuser(db, row['user_id']))

        return users


    def getuser(self, db, userid):
        cur = db.execute('select user_id, user_name, password, first_name, last_name, user_group_id from users where user_id = ?',[userid])
        usrs = cur.fetchall()
        usr = usrs[0]
        return user.User( usr['user_id'], usr['user_name'],usr['password'], usr['first_name'], usr['last_name'],usr['user_group_id'] )


    def validuser(self, db, username, password):
        cur = db.execute('select * from users where user_name = ? and password = ? ',[username, password])
        usrs = cur.fetchall()
        if len(usrs)>0:
            usr = usrs[0]
            return usr['user_id']
        else:
            return -1


    def createuser(self, db, username, password, firstname, lastname, usergroup):
        db.execute('insert into users (user_name, password, first_name, last_name, user_group_id) values (?, ?, ?, ? ,?)',
                 [username, password,firstname,lastname, usergroup])
        db.commit()


    def update_user(self, db, userid, username, password, firstname, lastname, usergroup):
        db.execute(
            'update users set user_name = ?, password = ?, first_name = ?, last_name = ?, user_group_id = ?, user_name = ? where user_id = ?',
            [username, password, firstname, lastname, usergroup, username, userid])
        db.commit()

