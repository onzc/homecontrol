import serialControl
import messagebuilder


class Device:
    deviceid = 0
    name = ''
    address = 0
    subid = 0
    devicetype = ''
    paired = False
    devicegroups = []


    def __init__(self, deviceid, name, address, subid, devicetype, paired, devicegroups):
        self.deviceid = deviceid
        self.name = name
        self.address = address
        self.subid = subid
        self.devicetype = devicetype
        self.paired = paired
        self.devicegroups = devicegroups

    def is_member_of_devicegroup(self, devicegroupid):
        r = False
        for devicegroup in self.devicegroups:
            if devicegroupid == devicegroup.devicegroupid:
                r = True
                break

        return r


    def pair(self, db):
        mb = messagebuilder.MessageBuilder()
        msg = mb.get_pair(self)
        sc = serialControl.SerialControl()
        sc.send_single_message(msg)
        cur = db.execute('update devices set paired = 1 where device_id = ?', [self.deviceid])
        db.commit()


    def unpair(self, db):
        mb = messagebuilder.MessageBuilder()
        msg = mb.get_unpair(self)
        sc = serialControl.SerialControl()
        sc.send_single_message(msg)
        cur = db.execute('update devices set paired = 0 where device_id = ?', [self.deviceid])
        db.commit()


    def on(self):
        mb = messagebuilder.MessageBuilder()
        msg = mb.get_on(self)
        sc = serialControl.SerialControl()
        sc.send_single_message(msg)


    def off(self):
        mb = messagebuilder.MessageBuilder()
        msg = mb.get_off(self)
        sc = serialControl.SerialControl()
        sc.send_single_message(msg)


    def dim_on(self):
        assert False  # not implemented yet
        pass


    def dim_off(self):
        assert False  # not implemented yet
        pass


    def dim_up(self):
        assert False  # not implemented yet
        pass


    def dim_down(self):
        assert False  # not implemented yet
        pass


    def dim_set(self, action):
        # action = dim_set_50
        level = int(action.replace('dim_set_', ''))
        assert level >= 0 and level <= 100
        assert False  # not implemented yet
        pass






