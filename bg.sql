-- DROP DATABASE IF EXISTS bg;
CREATE DATABASE  bg;

\c bg;

CREATE EXTENSION pgcrypto;
-- CREATE user main with login;

DROP TABLE IF EXISTS login;
CREATE TABLE login (
  email varchar(50) NOT NULL,
  fname text NOT NULL,
  lname text  NOT NULL,
  pw1 text NOT NULL,
  address text NOT NULL,
  city text NOT NULL,
  state text NOT NULL,
  zipcode varchar(5) NOT NULL
  );

INSERT INTO login (email, fname, lname, pw1, address, city, state, zipcode) VALUES ('scripture187@gmail.com','Billy', 'Andrews', crypt('pass', gen_salt('bf')), '78 C L Walker Blvd', 'Fredericksburg', 'VA', '22407');



GRANT SELECT, INSERT ON login TO bgtemp;



DROP TABLE IF EXISTS items;
CREATE TABLE items (
  productID int NOT NULL,
  name text NOT NULL,
  description text  NOT NULL,
  cost float NOT NULL,
  quantity int NOT NULL
  );
-- use two " '' " to use an apostrophe, like 'McCoy''s BBQ'
INSERT INTO items (productID, name, description, cost, quantity) VALUES (010789, 'Brake Cleaner', 'Cleans brake dust off metal parts', 3.99, 150);

GRANT SELECT ON items TO bgtemp;



DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
  fname text NOT NULL,
  lname text NOT NULL,
  message text NOT NULL,
  time timestamptz NOT NULL DEFAULT now()
  );

INSERT INTO messages (fname, lname, message) VALUES ('FaceBot','', 'Booting System...');
INSERT INTO messages (fname, lname, message) VALUES ('FaceBot','', 'FaceChat now LIVE!');

GRANT SELECT, INSERT ON messages TO bgtemp;

