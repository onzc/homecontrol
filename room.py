class Room:
    roomid = 0
    name = ''
    roomgroups = []
    devices = []

    def __init__(self, roomid, name, roomgroups, devices):
        self.roomid = roomid
        self.name = name
        self.roomgroups = roomgroups
        self.devices = devices


    def is_member_of_roomgroup(self, roomgroupid):
        r = False
        for roomgroup in self.roomgroups:
            if roomgroupid == roomgroup.roomgroupid:
                r = True
                break

        return r


    def remove_device(self, db, device):
        cur = db.execute('delete from room_device where room_id = ? and device_id = ?', [self.roomid, device.deviceid])
        db.commit()
        for d in self.devices:
            if d.deviceid == device.deviceid:
                self.devices.remove(d)


    def add_device(self, db, device):
        cur = db.execute('delete from room_device where room_id = ? and device_id = ?', [self.roomid, device.deviceid])
        db.commit()
        db.execute('INSERT INTO room_device ( room_id , device_id) VALUES (?, ?)', [self.roomid, device.deviceid])
        db.commit()
        self.devices.append(device)