INSERT INTO roomgroups (roomgroup_name)
VALUES ('Downstairs');

INSERT INTO roomgroups (roomgroup_name)
VALUES ('Upstairs');

INSERT INTO rooms (name )
VALUES ('Lounge' );

INSERT INTO room_roomgroup (roomgroup_id , room_id)
VALUES (1,1);

INSERT INTO rooms (name )
VALUES ('Kitchen' );

INSERT INTO room_roomgroup (roomgroup_id , room_id)
VALUES (1,2);

INSERT INTO users (user_name ,password, first_name, last_name , user_group_id)
VALUES ('admin' , 'p', 'admin', 'user' , 1);

INSERT INTO users (user_name ,password, first_name, last_name , user_group_id)
VALUES ('user' , 'p', 'registered', 'user' , 2);

INSERT INTO users (user_name ,password, first_name, last_name , user_group_id)
VALUES ('guest' , 'p', 'guest', 'user' , 3);