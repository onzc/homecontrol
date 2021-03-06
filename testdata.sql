INSERT INTO devicegroups (devicegroupname)
VALUES ('Sockets');

INSERT INTO devices (devicename, deviceaddress,devicesubid, paired, devicetype)
VALUES ('simple switch', 0, 13, 0, 'on_off');

INSERT INTO device_devicegroup (devicegroup_id ,device_id)
VALUES (1,1);

INSERT INTO devicegroups (devicegroupname)
VALUES ('Lights');

INSERT INTO devices (devicename, deviceaddress,devicesubid, paired, devicetype)
VALUES ('dimmer switch', 0, 12, 0, 'dimmer');

INSERT INTO device_devicegroup (devicegroup_id ,device_id)
VALUES (2,2);

INSERT INTO devices (devicename, deviceaddress,devicesubid, paired, devicetype)
VALUES ('test switch', 0, 12, 1, 'on_off');

INSERT INTO device_devicegroup (devicegroup_id ,device_id)
VALUES (1,3);

INSERT INTO roomgroups (roomgroup_name)
VALUES ('Downstairs');

INSERT INTO roomgroups (roomgroup_name)
VALUES ('Upstairs');

INSERT INTO rooms (name )
VALUES ('Lounge' );

INSERT INTO room_roomgroup (roomgroup_id , room_id)
VALUES (1,1);

INSERT INTO rooms (name )
VALUES ('Hall' );

INSERT INTO room_roomgroup (roomgroup_id , room_id)
VALUES (1,2);

INSERT INTO room_device (room_id, device_id)
VALUES (1,1);

INSERT INTO users (user_name ,password, first_name, last_name , user_group_id)
VALUES ('admin' , 'p', 'admin', 'user' , 1);

INSERT INTO users (user_name ,password, first_name, last_name , user_group_id)
VALUES ('user' , 'p', 'registered', 'user' , 2);

INSERT INTO users (user_name ,password, first_name, last_name , user_group_id)
VALUES ('guest' , 'p', 'guest', 'user' , 3);