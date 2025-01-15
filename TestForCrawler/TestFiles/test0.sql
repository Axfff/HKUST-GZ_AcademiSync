CREATE DATABASE test_university;
USE DATABASE test_university;
CREATE TABLE student (
    ID INTEGER,
    Name TEXT,
    GPA INTEGER,
    Major TEXT
);
SELECT * FROM student;
INSERT INTO student VALUES (1, 'Alice Johnson', 85, 'Computer Science');
INSERT INTO student VALUES (2, 'Bob Smith', 86, 'Electrical Engineering');
INSERT INTO student VALUES (3, 'Catherine Lee', 89, 'Mathematics');
INSERT INTO student VALUES (4, 'Dave Brown', 82, 'Physics');
INSERT INTO student VALUES (5, 'Eva White', 88, 'Chemistry');
SELECT * FROM student;