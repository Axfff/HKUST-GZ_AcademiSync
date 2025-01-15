CREATE DATABASE CompanyDB_4;
USE DATABASE CompanyDB_4;
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
INSERT INTO Employees VALUES (2, 'Jane', 'Doe', 2, 35);
INSERT INTO Employees VALUES (3, 'Jim', 'Beam', 3, 23);
INSERT INTO Employees VALUES (4, 'Jim', 'Doe', 2, 56);
INSERT INTO Employees VALUES (5, 'Jim', 'Eve', 2, 57);

SELECT * FROM Employees WHERE DepartmentID = 2;

UPDATE Employees SET DepartmentID = 3 WHERE EmployeeID = 2;

SELECT * FROM Employees;
SELECT * FROM Employees WHERE DepartmentID = 3 OR FirstName != 'John';
SELECT * FROM Employees WHERE EmployeeID > 3 AND FirstName = 'Jim';

SELECT Employees.FirstName, Employees.LastName, Departments.DepartmentName
FROM Employees
INNER JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID;