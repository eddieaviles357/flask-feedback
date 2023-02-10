-- from the terminal run:
-- psql < feedback.sql

DROP DATABASE IF EXISTS feedback;

CREATE DATABASE feedback;

\c feedback

CREATE TABLE users
(
    username VARCHAR(20) PRIMARY KEY UNIQUE,
    password TEXT NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL
);

INSERT INTO users ( username, password, email, first_name, last_name )
VALUES
('eddie123', 'eddieaviles123', 'eddie@yahoo.com', 'Eduardo', 'Aviles'),
('nancy123', 'nancyaviles123', 'nancy@yahoo.com', 'Nancy', 'Aviles'),
('eric123', 'ericaviles123', 'eric@yahoo.com', 'Eric','Aviles'),
('eddie1234','$2b$12$DxGUSeUO8T71X4waAGJvRODEXhqmXQmfk2wYAAdJeaSqTMZoizbYO', 'eddie1234@yahoo.com', 'Edward', 'Avile'),
('nancy1234','$2b$12$A89.yxoTFm/.iA3P9lJB1.wT1ejtzfihguyphNqIdSzpBzURq.z8O', 'nancy1234@yahoo.com', 'Nanc', 'Avile'),
('eric1234','$2b$12$HenQaqTWBtrO0bI7mffCU.ZyIrjVtBc8hY8nr5.mfVen80FtqzGK.', 'eric1234@yahoo.com', 'Eric', 'Avile');