import devicegroup


class DeviceGroupFactory():
    def get_devicegroups(self, db):
        cur = db.execute('select * from devicegroups')
        devicegroups = cur.fetchall()
        l = []
        for row in devicegroups:
            dg = devicegroup.DeviceGroup(row['devicegroup_id'], row['devicegroupname'])
            l.append(dg)

        return l


    def get_devicegroup(self, db, device):
        pass

