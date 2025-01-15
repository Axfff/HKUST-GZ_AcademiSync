CREATE DATABASE CompanyDB_5;
USE DATABASE CompanyDB_5;
CREATE TABLE Employees (
    EmployeeID INTEGER,
    FirstName TEXT,
    LastName TEXT,
    DepartmentID INTEGER,
    Age INTEGER
);

CREATE TABLE Departments (
    DepartmentID INTEGER,
    DepartmentName TEXT
);

INSERT INTO Departments VALUES (1, 'Human Resources');
INSERT INTO Departments VALUES (2, 'IT');
INSERT INTO Departments VALUES (3, 'Accounting');

INSERT INTO Employees VALUES (1, 'John', 'Doe', 1, 24);
INSERT INTO Employees VALUES (2, 'Jane', 'Doe', 3, 35);
INSERT INTO Employees VALUES (3, 'Jim', 'Beam', 3, 23);
INSERT INTO Employees VALUES (4, 'Jim', 'Doe', 2, 56);
INSERT INTO Employees VALUES (5, 'Jim', 'Eve', 2, 57);

SELECT Employees.FirstName, Employees.LastName, Employees.Age, Departments.DepartmentName
FROM Employees
INNER JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID;

INSERT INTO Employees VALUES (6, 'Kim', 'Brown', 1, 29);
INSERT INTO Employees VALUES (7, 'Eve', 'Jax', 2, 40);

SELECT * FROM Employees WHERE DepartmentID = 1 OR DepartmentID = 3;

UPDATE Employees SET DepartmentID = 1 WHERE DepartmentID = 3;

SELECT Employees.FirstName, Employees.LastName, Employees.Age, Departments.DepartmentName
FROM Employees
INNER JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID;

SELECT * FROM Employees WHERE Age > 34 AND DepartmentID = 2;

DELETE FROM Employees WHERE Age > 34 AND DepartmentID = 2;

SELECT Employees.FirstName, Employees.LastName, Employees.Age, Departments.DepartmentName
FROM Employees
INNER JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID;
