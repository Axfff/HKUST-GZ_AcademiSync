CREATE DATABASE test_university_2;
USE DATABASE test_university_2;
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
SELECT * FROM student;
UPDATE student SET GPA = GPA + 2 WHERE Name = 'Alice Johnson';
SELECT * FROM student WHERE Name = 'Alice Johnson';