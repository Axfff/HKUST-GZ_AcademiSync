
CREATE DATABASE companyDB_8;

USE DATABASE companyDB_8;

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

CREATE TABLE projects (
    project_id INTEGER,
    project_name TEXT,
    lead_id INTEGER
);

INSERT INTO employees VALUES (1, 'John Smith', 30, 1);
INSERT INTO employees VALUES (2, 'Jane Doe', 25, 2);
INSERT INTO employees VALUES (3, 'Alice Johnson', 28, 3);

INSERT INTO departments VALUES (1, 'Human Resources');
INSERT INTO departments VALUES (2, 'Finance');
INSERT INTO departments VALUES (3, 'IT');

INSERT INTO projects VALUES (101, 'Project Alpha', 1);
INSERT INTO projects VALUES (102, 'Project Beta', 2);
INSERT INTO projects VALUES (103, 'Project Gamma', 3);

SELECT * FROM employees;

SELECT * FROM employees WHERE age > 26;

UPDATE employees SET department_id = 2 WHERE id = 1;

SELECT * FROM employees WHERE age > 25 AND department_id = 2;
SELECT * FROM employees WHERE age > 25 OR department_id = 3;

SELECT employees.name, departments.department_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.department_id;

SELECT employees.name, departments.department_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.department_id
WHERE employees.age > 25 AND departments.department_name = 'IT';

SELECT employees.name, departments.department_name, projects.project_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.department_id
INNER JOIN projects ON employees.id = projects.lead_id;