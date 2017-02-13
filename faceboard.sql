DROP DATABASE IF EXISTS faceboard;
CREATE DATABASE  faceboard;

\c faceboard;

CREATE EXTENSION pgcrypto;
CREATE user faceboardtemp with login;

DROP TABLE IF EXISTS login;
CREATE TABLE login (
  fname varchar(25) NOT NULL,
  lname varchar(35)  NOT NULL,
  email varchar(50) NOT NULL,
  dob date,
  pw1 varchar(50) NOT NULL
  );

INSERT INTO login (fname, lname, email, dob, pw1) VALUES ('Billy', 'Andrews', 'scripture187@gmail.com', '1984-10-10','WA.army.07');
INSERT INTO login (fname, lname, email, dob, pw1) VALUES ('Whitney', 'Esposito', 'wespo796@gmail.com', '1990-02-12','pass');
INSERT INTO login (fname, lname, email, dob, pw1) VALUES ('Justina', 'Andrews', 'salsijustini@gmail.com', '1980-02-11','pass');


GRANT SELECT, INSERT ON login TO faceboardtemp;


