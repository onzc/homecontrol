/*
INSERT INTO rooms (name)
VALUES ('Lounge' );

INSERT INTO rooms (name)
VALUES ('Kitchen' );
*/
INSERT INTO users (user_name ,password, first_name, last_name , user_group_id)
VALUES ('admin' , 'p', 'admin', 'user' , 1);

INSERT INTO users (user_name ,password, first_name, last_name , user_group_id)
VALUES ('user' , 'p', 'registered', 'user' , 2);

INSERT INTO users (user_name ,password, first_name, last_name , user_group_id)
VALUES ('guest' , 'p', 'guest', 'user' , 3);