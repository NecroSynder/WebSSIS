
-- mySQL query
DROP DATABASE IF EXISTS ssis;
CREATE DATABASE IF NOT EXISTS ssis;
use ssis;

DROP TABLE IF EXISTS college;
CREATE TABLE IF NOT EXISTS college(
code VARCHAR(10) NOT NULL,
name VARCHAR(50) NOT NULL,
PRIMARY KEY(code)
);

DROP TABLE IF EXISTS course;
CREATE TABLE IF NOT EXISTS course(
code VARCHAR(10) NOT NULL,
name VARCHAR(50) NOT NULL,
college_code VARCHAR(10) NOT NULL,
PRIMARY KEY(code),
FOREIGN KEY(college_code) REFERENCES college(code)
);

DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student(
id VARCHAR(10) NOT NULL,
firstname VARCHAR(100) NOT NULL,
lastname VARCHAR(100) NOT NULL,
course_code VARCHAR(10) NOT NULL,
year INT NOT NULL,
gender VARCHAR(10) NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(course_code) REFERENCES course(code)
);

