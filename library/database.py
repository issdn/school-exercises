import sqlite3 as sql

"""
    Don't how to refactor add_row and update better.
"""

class Database:
    def __init__(self, db_path: str = 'library'):
        self.db: sql.Connection = sql.connect(db_path)
        self.cur: sql.Cursor = self.db.cursor()

    def add_schema(self, path: str = 'schema.sql') -> None: 
        with open(path) as f:
            self.db.executescript(f.read())

    def add_row(self, table_name: str, row: dict):
        if table_name == "books":
            self.cur.execute("INSERT INTO books (title) VALUES (?)", (row["title"],))
        if table_name == "users":
            self.cur.execute("INSERT INTO users (name, surname) VALUES (?, ?)", (row["name"], row["surname"],))
        if table_name == "borrowed":
            self.cur.execute("INSERT INTO borrowed (book_id, user_id) VALUES (?, ?)", (row["book_id"], row["user_id"],))
        self.db.commit()

    def update(self, table_name: str, row: dict) -> None:
        if table_name == "books":
            self.cur.execute("UPDATE books SET title = ? WHERE id = ?", (row["title"], row["id"],))
        if table_name == "users":
            self.cur.execute("UPDATE users SET name = ?, surname = ? WHERE id = ?", (row["name"], row["surname"], row["id"],))
        if table_name == "borrowed":
            self.cur.execute("UPDATE borrowed SET book_id = ?, user_id = ? WHERE id = ?", (row["book_id"], row["user_id"], row["id"],))
        self.db.commit()

    def delete(self, table_name: str, id: dict) -> None:
        self.cur.execute(f"DELETE FROM {table_name} WHERE id = ?", (str(id), ))
        self.db.commit()

    def fetch_table(self, table: str) -> list:
        self.cur.execute(f"SELECT * FROM {table}")
        return self.cur.fetchall()
    
    def fetch_all_tables(self) -> list:
        cursor = self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE'sqlite_%'")
        return [table_title[0] for table_title in cursor]

    def fetch_columns(self, table: str) -> list:
        return [column[1] for column in self.db.execute(f"PRAGMA table_info({table})")]
    
