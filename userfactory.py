import homecontrol
import user
import flask


class Userfactory():

    def getusers(self, db):
        cur = db.execute('select user_id, user_name, password, first_name, last_name from users')
        usr = cur.fetchall()
        return usr


    def newuser(self, db, userid):
        cur = db.execute('select user_id, user_name, password, first_name, last_name, user_group_id from users where user_id = ?',[userid])
        usrs = cur.fetchall()
        usr = usrs[0]
        return user.User(self, usr['user_id'], usr['user_name'],usr['password'], usr['first_name'], usr['last_name'] )


    def validuser(self, db, username, password):
        cur = db.execute('select * from users where user_name = ? and password = ? ',[username, password])
        usr = cur.fetchall()
        if len(usr)>0:
            return True
        else:
            return False


    def createuser(self, db, username, password, firstname, lastname, usergroup):
        db.execute('insert into users (user_name, password, first_name, last_name, user_group_id) values (?, ?, ?, ? ,?)',
                 [username, password,firstname,lastname, usergroup])
        db.commit()
