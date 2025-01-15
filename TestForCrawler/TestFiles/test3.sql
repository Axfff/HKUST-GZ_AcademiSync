CREATE DATABASE test_university_3;
USE DATABASE test_university_3;
CREATE TABLE student (
    ID INTEGER,
    Name TEXT,
    GPA INTEGER,
    Major TEXT
);
INSERT INTO student VALUES (1, 'Alice Johnson', 85, 'Computer Science');
INSERT INTO student VALUES (2, 'Bob Smith', 86, 'Electrical Engineering');
INSERT INTO student VALUES (3, 'Catherine Lee', 89, 'Mathematics');
INSERT INTO student VALUES (4, 'Dave Brown', 82, 'Physics');
INSERT INTO student VALUES (5, 'Eva White', 88, 'Chemistry');
INSERT INTO student VALUES (6, 'Elle Flores', 82, 'Physics');
INSERT INTO student VALUES (7, 'Ina Rodriguez', 85, 'Chemistry');
SELECT * FROM student;
UPDATE student SET GPA = GPA - 1 WHERE Name = 'Elle Flores';
SELECT * FROM student WHERE Name = 'Elle Flores';