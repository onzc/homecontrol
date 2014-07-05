import room


class Roomfactory():
    def getrooms(self, db):
        cur = db.execute('select room_id, name from rooms order by room_id asc')
        rooms = cur.fetchall()
        return rooms


    def getroom(self, db, roomid):
        cur = db.execute(
            'select room_id, name , roomgroup_id , roomgroup_name  from rooms natural join room_roomgroup natural join roomgroups where room_id = ?',
            [roomid])
        rooms = cur.fetchall()
        rm = rooms[0]
        return room.Room(rm['room_id'], rm['name'], rm['roomgroup_id'], rm['roomgroup_name'])

    def createroom(self, db, name, roomgroups):
        cur = db.execute('INSERT INTO rooms (name) VALUES (?)', [name])
        roomid = cur.lastrowid
        for roomgroupid in roomgroups:
            cur = db.execute('INSERT INTO room_roomgroup (roomgroup_id , room_id) VALUES (?,?)', [roomgroupid, roomid])
        db.commit()
        return roomid