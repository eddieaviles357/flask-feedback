-- from the terminal run:
-- psql < feedback.sql

DROP DATABASE IF EXISTS feedback;

CREATE DATABASE feedback;

\c feedback

CREATE TABLE user
(
    username PRIMARY KEY UNIQUE,
    password TEXT NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL
);

INSERT INTO user ( username, password, email, first_name, last_name )
VALUES
('eddie123', 'eddieaviles123', 'eddie@yahoo.com', 'Eduardo', 'Aviles'),
('nancy123', 'nancyaviles123', 'nancy@yahoo.com', 'Nancy', 'Aviles'),
('eric123', 'ericaviles123', 'eric@yahoo.com', 'Eric','Aviles');