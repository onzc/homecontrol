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
        msg = mb.build_simple_message('PAIR', self.address, self.subid, 0, 0, 1)
        sc = serialControl.SerialControl()
        sc.send_single_message(msg)
        cur = db.execute('update devices set paired = 1 where device_id = ?', [self.deviceid])
        db.commit()


    def unpair(self, db):
        mb = messagebuilder.MessageBuilder()
        msg = mb.build_simple_message('PAIR', self.address, self.subid, 0, 0, 0)
        sc = serialControl.SerialControl()
        sc.send_single_message(msg)
        cur = db.execute('update devices set paired = 0 where device_id = ?', [self.deviceid])
        db.commit()


    def on(self):
        mb = messagebuilder.MessageBuilder()
        msg = mb.build_simple_message('SEND', self.address, self.subid, 0, 0, 1)
        sc = serialControl.SerialControl()
        sc.send_single_message(msg)


    def off(self):
        mb = messagebuilder.MessageBuilder()
        msg = mb.build_simple_message('SEND', self.address, self.subid, 0, 0, 0)
        sc = serialControl.SerialControl()
        sc.send_single_message(msg)


    def xx(self):
        pass


