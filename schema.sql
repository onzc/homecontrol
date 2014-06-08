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
