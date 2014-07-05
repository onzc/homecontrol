class Room:
    roomid = 0
    name = ''
    roomgroupid = 0,
    roomgroupname = ''

    def __init__(self, roomid, name, roomgroupid, roomgroupname):
        self.roomid = roomid
        self.name = name
        self.roomgroupid = roomgroupid
        self.roomgroupname = roomgroupname
