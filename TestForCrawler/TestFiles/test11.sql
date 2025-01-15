USE DATABASE CompanyDB_4;

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