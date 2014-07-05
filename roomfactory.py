import room
import roomgroupfactory
import roomgroup

class Roomfactory():
    def getrooms(self, db):
        cur = db.execute('select room_id, name from rooms order by room_id asc')
        roomsrows = cur.fetchall()
        rooms = []
        for roomsrow in roomsrows:
            room = self.getroom(db, roomsrow['room_id'])
            rooms.append(room)
        return rooms


    def getroom(self, db, roomid):
        cur = db.execute(
            'select room_id, name from rooms where room_id = ?', [roomid])
        rooms = cur.fetchall()
        rm = rooms[0]
        cur = db.execute(
            'select room_roomgroup.roomgroup_id, room_roomgroup.room_id, roomgroups.roomgroup_name from room_roomgroup natural join roomgroups where room_roomgroup.room_id =?',
            [roomid])
        roomgrouprows = cur.fetchall()
        roomgroups = []
        rgf = roomgroupfactory.Roomgroupfactory
        for row in roomgrouprows:
            rmgrp = roomgroup.Roomgroup(row['roomgroup_id'], row['roomgroup_name'])
            roomgroups.append(rmgrp)

        return room.Room(rm['room_id'], rm['name'], roomgroups)

    def createroom(self, db, name, roomgroups):
        cur = db.execute('INSERT INTO rooms (name) VALUES (?)', [name])
        roomid = cur.lastrowid
        for roomgroupid in roomgroups:
            cur = db.execute('INSERT INTO room_roomgroup (roomgroup_id , room_id) VALUES (?,?)', [roomgroupid, roomid])
        db.commit()
        return roomid