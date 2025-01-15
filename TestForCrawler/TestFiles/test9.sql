CREATE DATABASE libraryDB_9;

USE DATABASE libraryDB_9;

CREATE TABLE books (
    book_id INTEGER,
    title TEXT,
    author_id INTEGER,
    is_available INTEGER
);

CREATE TABLE authors (
    author_id INTEGER,
    author_name TEXT
);

CREATE TABLE loans (
    loan_id INTEGER,
    book_id INTEGER,
    loan_date TEXT,
    return_date TEXT,
    is_returned INTEGER
);

INSERT INTO authors VALUES (1, 'George Orwell');
INSERT INTO authors VALUES (2, 'Virginia Woolf');
INSERT INTO authors VALUES (3, 'James Joyce');

INSERT INTO books VALUES (101, '1984', 1, 1);
INSERT INTO books VALUES (102, 'Mrs Dalloway', 2, 1);
INSERT INTO books VALUES (103, 'Ulysses', 3, 0);

INSERT INTO loans VALUES (201, 103, '2024-01-01', '2024-01-15', 0);
INSERT INTO loans VALUES (202, 101, '2024-01-02', '2024-01-20', 0);
INSERT INTO loans VALUES (203, 102, '2024-01-21', '2024-01-22', 1);
INSERT INTO loans VALUES (202, 102, '2024-01-23', '2024-01-25', 0);

SELECT * FROM books;

SELECT * FROM books WHERE is_available = 1;

UPDATE books SET is_available = 0 WHERE book_id = 102;

SELECT books.title, authors.author_name FROM books
INNER JOIN authors ON books.author_id = authors.author_id
WHERE books.is_available = 1 AND authors.author_name = 'Virginia Woolf';

SELECT books.title, authors.author_name
FROM books
INNER JOIN authors ON books.author_id = authors.author_id;

SELECT books.title, loans.loan_date, loans.return_date
FROM books
INNER JOIN loans ON books.book_id = loans.book_id
WHERE loans.is_returned = 0 AND (loans.return_date = '2024-01-15' OR loans.return_date = '2024-01-25');