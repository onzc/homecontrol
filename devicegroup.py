import serialControl
import messagebuilder


class DeviceGroup:
    devicegroupid = 0
    name = ''
    devices = []


    def on(self):
        for device in self.devices:
            device.on()
            # mb = messagebuilder.MessageBuilder()
            # msg = mb.get_device_group_on(self.devices)
            # print(msg)
            # sc = serialControl.SerialControl()
            # sc.send_single_message(msg)


    def off(self):
        for device in self.devices:
            device.off()
            # mb = messagebuilder.MessageBuilder()
            # msg = mb.get_device_group_off(self.devices)
            # print(msg)
            # sc = serialControl.SerialControl()
            # sc.send_single_message(msg)


    def __init__(self, devicegroupid, name, devices):
        self.devicegroupid = devicegroupid
        self.name = name
        self.devices = devices