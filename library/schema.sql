DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS borrowed;

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT CHECK(title <> '')
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT CHECK(name <> ''),
    surname TEXT CHECK(surname <> '')
);

CREATE TABLE borrowed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrowed_at TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    end_date DATE DEFAULT (DATE('now', '+1 months')),
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
