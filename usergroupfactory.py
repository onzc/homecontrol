import usergroup


class UserGroupFactory():
    def get_user_groups(self, db):
        cur = db.execute('select user_group_id from user_groups')
        rows = cur.fetchall()
        usergroups = []
        for row in rows:
            user_group_id = row['user_group_id']
            usergroup = self.get_user_group(db, user_group_id)
            usergroups.append(usergroup)

        return usergroups

    def get_user_group(self, db, user_group_id):
        cur = db.execute('select * from user_groups where user_group_id = ?', [user_group_id])
        rows = cur.fetchall()
        row = rows[0]
        return usergroup.UserGroup(user_group_id, row['group_name'])

