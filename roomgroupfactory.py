import roomgroup


class Roomgroupfactory:
    def getroomgroups(self, db):
        cur = db.execute('select roomgroup_id, roomgroup_name from roomgroups')
        roomgroups = cur.fetchall()
        l = []
        for row in roomgroups:
            rg = roomgroup.Roomgroup(row['roomgroup_id'], row['roomgroup_name'])
            l.append(rg)

        return l


    def getroomgroup(self, roomgroupid, name):
        return roomgroup.Roomgroup(roomgroupid, name)
