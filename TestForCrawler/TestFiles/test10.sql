CREATE DATABASE test_university_10;
USE DATABASE test_university_10;
CREATE TABLE student (
    ID INTEGER,
    Name TEXT,
    GPA FLOAT,
    Major TEXT
);
SELECT * FROM student;
INSERT INTO student VALUES (1, 'Alice Johnson', 3.5, 'Computer Science');
INSERT INTO student VALUES (2, 'Bob Smith', 3.6, 'Electrical Engineering');
INSERT INTO student VALUES (3, 'Catherine Lee', 3.9, 'Mathematics');
INSERT INTO student VALUES (4, 'Dave Brown', 3.2, 'Physics');
INSERT INTO student VALUES (5, 'Eva White', 3.8, 'Chemistry');
SELECT * FROM student;