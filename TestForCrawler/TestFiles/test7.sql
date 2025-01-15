CREATE DATABASE CompanyDB_7;
USE DATABASE CompanyDB_7;

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

INSERT INTO employees VALUES (1, 'John Doe', 30, 102);
INSERT INTO employees VALUES (2, 'Jane Smith', 25, 102);
INSERT INTO employees VALUES (3, 'Alice Johnson', 28, 103);

INSERT INTO departments VALUES (101, 'Human Resources');
INSERT INTO departments VALUES (102, 'Finance');
INSERT INTO departments  VALUES (103, 'IT');

INSERT INTO employees VALUES (4, 'Mike Brown', 32, 101);
INSERT INTO employees VALUES (5, 'Lisa Ray', 27, 102);

INSERT INTO departments VALUES (104, 'Marketing');

SELECT * FROM employees;

SELECT * FROM employees WHERE age > 26;

UPDATE employees SET department_id = 104 WHERE id = 2;

SELECT * FROM employees WHERE age > 26 AND department_id = 103;
SELECT * FROM employees WHERE age > 26 OR department_id = 104;

SELECT employees.name, departments.department_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.department_id;

SELECT employees.name, departments.department_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.department_id
WHERE employees.age > 25 AND departments.department_name = 'IT';

SELECT employees.name, employees.age, departments.department_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.department_id
WHERE departments.department_name = 'Finance' OR employees.age > 25;

UPDATE employees SET age = age + 1 WHERE department_id = 101 OR department_id = 102;

DELETE FROM departments WHERE department_id = 104;

SELECT * FROM departments;