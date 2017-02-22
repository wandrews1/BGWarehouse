DROP DATABASE IF EXISTS faceboard;
CREATE DATABASE  faceboard;

\c faceboard;

CREATE EXTENSION pgcrypto;
-- CREATE user faceboardtemp with login;

DROP TABLE IF EXISTS login;
CREATE TABLE login (
  fname text NOT NULL,
  lname text  NOT NULL,
  email varchar(50) NOT NULL,
  dob date,
  zipcode numeric(5,0) NOT NULL,
  pw1 text NOT NULL
  );

INSERT INTO login (fname, lname, email, dob, zipcode, pw1) VALUES ('Billy', 'Andrews', 'scripture187@gmail.com', '1984-10-10',22407,crypt('pass', gen_salt('bf')));
INSERT INTO login (fname, lname, email, dob, zipcode, pw1) VALUES ('Whitney', 'Esposito', 'wespo796@gmail.com', '1990-02-12',22407,crypt('pass', gen_salt('bf')));
INSERT INTO login (fname, lname, email, dob, zipcode, pw1) VALUES ('Justina', 'Andrews', 'salsijustini@gmail.com', '1980-02-11',22407,crypt('pass', gen_salt('bf')));


GRANT SELECT, INSERT ON login TO faceboardtemp;



DROP TABLE IF EXISTS places;
CREATE TABLE places (
  name text NOT NULL,
  category text  NOT NULL,
  subcategory text NOT NULL,
  address text NOT NULL,
  city text NOT NULL,
  state varchar(2) NOT NULL,
  country text NOT NULL DEFAULT 'USA',
  phone numeric(12,0) NOT NULL,
  zipcode numeric(5,0) NOT NULL
  );

INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('McCoy''s BBQ', 'Food', 'BBQ', '5151 Plank Rd', 'Fredericksburg','VA','USA',5407607078,22407);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('El Pino Mexican Restaurant', 'Food', 'Mexican', '4211 Plank Rd', 'Fredericksburg','VA','USA',5405484332,22407);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('Pho Saigon Vietnamese Restaurant', 'Food', 'Vietnamese', '2601 Salem Church Rd', 'Fredericksburg','VA','USA',5407852988,22407);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('Basilico', 'Food', 'Italian Deli', '2577 Cowan Blvd', 'Fredericksburg','VA','USA',5403700355,22401);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('Taj Indian Cuisine', 'Food', 'Indian', '2032 Plank Rd', 'Fredericksburg','VA','USA',5406562884,22401);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('Fujiya House', 'Food', 'Japanese', '1489 Carl D Silver Pkwy', 'Fredericksburg','VA','USA',5407850011,22401);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('Firebirds Wood Fired Grill', 'Food', 'Steakhouse', '1 Towne Center Blvd', 'Fredericksburg','VA','USA',5405485100,22407);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('El Torito Taqueria''s BBQ', 'Food', 'Mexican', '2601 Salem Church Rd', 'Fredericksburg','VA','USA',5404120560,22407);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('Agora Downtown', 'Food', 'Coffee', '520 Caroline St', 'Fredericksburg','VA','USA',5403698180,22401);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('Miso Asian Grill & Sushi Bar', 'Food', 'Japanese', '5151 Plank Rd', 'Fredericksburg','VA','USA',5407607078,22407);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('Park Lane Tavern', 'Food', 'British Pub', '1 Towne Center Blvd', 'Fredericksburg','VA','USA',5405480550,22407);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('Wawa', 'Convenience', 'Gas', '10626-1063 Courthouse Rd', 'Fredericksburg','VA','USA',5408984278,22407);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('CVS', 'Convenience', 'Pharmacy', '10701 Courthouse Rd', 'Fredericksburg','VA','USA',5408982117,22407);
INSERT INTO places (name, category, subcategory, address, city, state, country, phone, zipcode) VALUES ('American Family Fitness', 'Fitness', 'Gym', '10020 Southpoint Pkwy', 'Fredericksburg','VA','USA',5408986111,22407);



GRANT SELECT ON places TO faceboardtemp;


