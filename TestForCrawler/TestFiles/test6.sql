CREATE DATABASE CompanyDB_6;
USE DATABASE CompanyDB_6;

CREATE TABLE employees (
    id INTEGER,
    name TEXT,
    age INTEGER,
    department_id INTEGER
);

CREATE TABLE departments (
    department_id INTEGER,
    department_name TEXT
);

INSERT INTO employees VALUES (1, 'John Doe', 30, 101);
INSERT INTO employees VALUES (2, 'Jane Smith', 25, 102);
INSERT INTO employees VALUES (3, 'Alice Johnson', 28, 103);

INSERT INTO departments VALUES (101, 'Human Resources');
INSERT INTO departments VALUES (102, 'Finance');
INSERT INTO departments  VALUES (103, 'IT');

SELECT * FROM employees;

SELECT * FROM employees WHERE age > 26;

UPDATE employees SET department_id = 102 WHERE id = 1;

SELECT * FROM employees WHERE age > 26 AND department_id = 103;
SELECT * FROM employees WHERE age > 26 OR department_id = 102;

SELECT employees.name, departments.department_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.department_id;

SELECT employees.name, departments.department_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.department_id
WHERE employees.age > 25 AND departments.department_name = 'IT';