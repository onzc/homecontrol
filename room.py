class Room:
    roomid = 0
    name = ''
    roomgroups = []

    def __init__(self, roomid, name, roomgroups):
        self.roomid = roomid
        self.name = name
        self.roomgroups = roomgroups


    def is_member_of_roomgroup(self, roomgroupid):
        r = False
        for roomgroup in self.roomgroups:
            if roomgroupid == roomgroup.roomgroupid:
                r = True
                break

        return r