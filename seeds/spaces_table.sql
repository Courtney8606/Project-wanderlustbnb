-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

DROP TABLE IF EXISTS spaces;
DROP SEQUENCE IF EXISTS spaces_id_seq;
DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS bookings_id_seq;
DROP TABLE IF EXISTS upload;
DROP SEQUENCE IF EXISTS upload_id_seq;

CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE spaces (
  id SERIAL PRIMARY KEY,
  name text,
  location text,
  price float,
  description text,
  user_id int,
  image_title text
);

CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username text,
  name text,
  password text
);

CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE bookings (
  id SERIAL PRIMARY KEY,
  space_id int,
  date_booked date,
  userid_booker int,
  userid_approver int,
  approved bool DEFAULT false,
  display_message_icon bool
);

CREATE SEQUENCE IF NOT EXISTS upload_id_seq;
CREATE TABLE upload (
    id SERIAL PRIMARY KEY,
    title VARCHAR( 100 ) NOT NULL
);

-- Add any records that are needed for the tests to run

INSERT INTO spaces (name, location, price, description, user_id, image_title) VALUES ('Wizarding Cupboard', 'London', 50.00, 'A cosy room under the stairs. Comes with complementary spiders.', 1, 'house1.jpg');
INSERT INTO spaces (name, location, price, description, user_id, image_title) VALUES ('Amore Penthouse', 'Paris', 87.00, 'Within view of the Eiffel Tower, this penthouse is your parisian dream.', 2, 'house2.jpg');
INSERT INTO spaces (name, location, price, description, user_id, image_title) VALUES ('Paella Place', 'Madrid', 31.59, 'Eat paella and sleep.', 3, 'house3.jpg');
INSERT INTO spaces (name, location, price, description, user_id, image_title) VALUES ('Mi Casa', 'Madrid', 45.50, 'Es tu Casa.', 3, 'house4.jpg');

INSERT INTO users (username, name, password) VALUES ('mrs_dursley', 'Petunia Dursley', 'hatemynephew123');
INSERT INTO users (username, name, password) VALUES ('ratatouille', 'Remy Rat', 'kissthecook');
INSERT INTO users (username, name, password) VALUES ('montoya', 'Inigo Montoya', 'prepare2die');

INSERT INTO bookings (space_id, date_booked, userid_booker, userid_approver, approved, display_message_icon) VALUES (4, '2024-07-12', 1, 3, False, False);
INSERT INTO bookings (space_id, date_booked, userid_booker, userid_approver, approved, display_message_icon) VALUES (3, '2024-07-12', 2, 3, False, False);
INSERT INTO bookings (space_id, date_booked, userid_booker, userid_approver, approved, display_message_icon) VALUES (2, '2024-07-12', 1, 2, True, True);

INSERT INTO upload (title) VALUES ('house1.jpg');
INSERT INTO upload (title) VALUES ('house2.jpg');
INSERT INTO upload (title) VALUES ('house3.jpg');
INSERT INTO upload (title) VALUES ('house4.jpg');

