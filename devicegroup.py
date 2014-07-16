class DeviceGroup:
    devicegroupid = 0
    name = ''
    devices = []

    def __init__(self, devicegroupid, name):
        self.devicegroupid = devicegroupid
        self.name = name
        # self.devices = devices