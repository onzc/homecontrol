drop table if exists room_device;
create table room_device (
    room_device_id integer primary key autoincrement,
    room_id integer,
    device_id integer
);
drop table if exists devices;
create table devices (
    device_id integer primary key autoincrement,
    devicename text not null,
    deviceaddress integer not null,
    devicesubid int not null,
    paired int not null,
    devicetype text not null
);

drop table if exists devicegroups;
create table devicegroups (
    devicegroup_id integer primary key autoincrement,
    devicegroupname text not null
);

drop table if exists device_devicegroup;
create table device_devicegroup (
    device_devicegroup_id integer primary key autoincrement,
    devicegroup_id integer,
    device_id integer
);

drop table if exists room_roomgroup;
create table room_roomgroup (
    room_roomgroup_id integer primary key autoincrement,
    roomgroup_id int,
    room_id int
);


drop table if exists roomgroups;
create table roomgroups (
    roomgroup_id integer primary key autoincrement,
    roomgroup_name text not null
);

drop table if exists rooms;
create table rooms (
  room_id integer primary key autoincrement,
  name text not null
);


drop table if exists users;
create table users (
    user_id integer primary key autoincrement,
    user_name text not null,
    password text not null,
    first_name text not null,
    last_name text not null,
    user_group_id integer
);


drop table if exists user_groups;
create table user_groups (
    user_group_id integer primary key,
    group_name text not null
);
