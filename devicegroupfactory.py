import devicegroup
import devicefactory


class DeviceGroupFactory():
    def get_devicegroups(self, db):
        cur = db.execute('select * from devicegroups')
        devicegroups = cur.fetchall()
        l = []
        for row in devicegroups:
            # dg = devicegroup.DeviceGroup(row['devicegroup_id'], row['devicegroupname'])
            dg = self.get_devicegroup(db, row['devicegroup_id'])
            l.append(dg)

        return l


    def get_devicegroup(self, db, devicegroup_id):
        cur = db.execute('select * from devicegroups where devicegroup_id = ?', [devicegroup_id])
        devicegroups = cur.fetchall()
        dg = devicegroups[0]
        return self.__get_dg(db, devicegroup_id, dg['devicegroupname'])


    def __get_dg(self, db, devicegroup_id, devicegroup_name):

        cur = db.execute('select * from device_devicegroup where device_devicegroup.devicegroup_id = ?',
                         [devicegroup_id])
        rows = cur.fetchall()
        df = devicefactory.DeviceFactory()
        devices = []
        for row in rows:
            device = df.get_device(db, row['device_id'])
            devices.append(device)

        dg = devicegroup.DeviceGroup(devicegroup_id, devicegroup_name, devices)
        return dg

