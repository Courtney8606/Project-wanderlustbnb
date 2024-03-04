-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

CREATE TABLE spaces (
  id SERIAL PRIMARY KEY,
  name text,
  booking_date date,
  location text,
  price float,
  description text,
  user_id int
);

-- Finally, we add any records that are needed for the tests to run
INSERT INTO spaces (id, name, date_booked, location, user_id) VALUES (1, 'appt 1', '2024-05-12', 'london', 50.00, 'jbvsdjh', 1);
INSERT INTO spaces (id, name, date_booked, location, user_id) VALUES (2, 'appt 2', '2024-07-12', 'paris', 87.00, 'djfhfh', 2);