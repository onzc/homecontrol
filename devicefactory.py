import device
import devicegroup
import devicegroupfactory


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
            dvgroup = devicegroup.DeviceGroup(grouprow['devicegroup_id'], grouprow['devicegroupname'], None)
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


    def get_available_devices(self, db, room):
        cur = db.execute('select * from devices')
        devicerows = cur.fetchall()
        devices = []
        existing_deviceids = []
        for existingdevice in room.devices:
            existing_deviceids.append(existingdevice.deviceid)

        for row in devicerows:
            deviceid = row['device_id']

            if deviceid not in existing_deviceids:
                d = self.get_device(db, deviceid)
                devices.append(d)

        return devices


    def get_next_available_device_address(self, db):
        address = -1
        subid = -1

        for a in range(16):
            for s in range(16):
                cur = db.execute('select device_id from devices where deviceaddress = ? and devicesubid= ?', [a, s])
                rows = cur.fetchall()
                if len(rows) == 0:
                    address = a
                    subid = s
                    break

            if subid != -1:
                break

        dict = {'deviceaddress': address, 'subid': subid}
        return dict