import device
import devicegroup


class DeviceFactory():
    def get_devices(self, db):
        cur = db.execute('select * from devices')
        devicerows = cur.fetchall()
        devices = []
        for row in devicerows:
            d = self.get_device(db, row['device_id'])
            devices.append(d)

        return devices


    def get_device(self, db, deviceid):
        cur = db.execute(
            'select * from devices where device_id = ?', [deviceid])
        rows = cur.fetchall()
        row = rows[0]
        devicegroups = []
        cur = db.execute(
            'select device_devicegroup.device_devicegroup_id , device_devicegroup.devicegroup_id, device_devicegroup.device_id, devicegroups.devicegroupname from device_devicegroup natural join devicegroups where device_devicegroup.device_id = ?',
            [deviceid])
        grouprows = cur.fetchall()

        for grouprow in grouprows:
            dvgroup = devicegroup.DeviceGroup(grouprow['devicegroup_id'], grouprow['devicegroupname'])
            devicegroups.append(dvgroup)

        return device.Device(row['device_id'], row['devicename'], row['deviceaddress'], row['devicesubid'],
                             row['devicetype'], row['paired'], devicegroups)


    def create(self, db, name, address, subid, type, paired, devicegroups):
        cur = db.execute(
            'INSERT INTO devices (devicename, deviceaddress, devicesubid, devicetype, paired) VALUES (?,?,?,?, ?)',
            [name, address, subid, type, paired])
        deviceid = cur.lastrowid
        for devicegroupid in devicegroups:
            cur = db.execute('INSERT INTO device_devicegroup (devicegroup_id , device_id) VALUES (?,?)',
                             [devicegroupid, deviceid])
        db.commit()
        return deviceid


    def update(self, db, deviceid, name, address, subid, type, paired, devicegroups):
        cur = db.execute(
            'update devices set devicename= ?, deviceaddress= ?, devicesubid = ?, devicetype = ?, paired = ?  where device_id= ?',
            [name, address, subid, type, paired, deviceid])
        cur = db.execute('delete from device_devicegroup where device_devicegroup.device_id = ?', [deviceid])
        for devicegroupid in devicegroups:
            cur = db.execute('INSERT INTO device_devicegroup (devicegroup_id , device_id) VALUES (?,?)',
                             [devicegroupid, deviceid])
        db.commit()


    def delete(self, db, deviceid):
        cur = db.execute('delete from devices where device_id =?', [deviceid])
        cur = db.execute('delete from device_devicegroup where device_id =?', [deviceid])
        db.commit()