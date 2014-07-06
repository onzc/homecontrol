import room
import roomgroupfactory
import roomgroup


class RoomFactory():
    def get_rooms(self, db):
        cur = db.execute('select room_id, name from rooms order by room_id asc')
        roomsrows = cur.fetchall()
        rooms = []
        for roomsrow in roomsrows:
            room = self.get_room(db, roomsrow['room_id'])
            rooms.append(room)
        return rooms


    def get_room(self, db, roomid):
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


    def update_room(self, db, roomid, name, roomgroups):
        cur = db.execute('update rooms set name= ? where room_id= ?', [name, roomid])
        cur = db.execute('delete from room_roomgroup where room_roomgroup.room_id = ?', [roomid])
        for roomgroupid in roomgroups:
            cur = db.execute('INSERT INTO room_roomgroup (roomgroup_id , room_id) VALUES (?,?)', [roomgroupid, roomid])
        db.commit()


    def create_room(self, db, name, roomgroups):
        cur = db.execute('INSERT INTO rooms (name) VALUES (?)', [name])
        roomid = cur.lastrowid
        for roomgroupid in roomgroups:
            cur = db.execute('INSERT INTO room_roomgroup (roomgroup_id , room_id) VALUES (?,?)', [roomgroupid, roomid])
        db.commit()
        return roomid


    def delete_room(self, db, roomid):
        cur = db.execute('delete from rooms where rooms.room_id =?', [roomid])
        db.commit()