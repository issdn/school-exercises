import sqlite3 as sql
import os

class Database:
    DB: sql.Connection = None
    CUR: sql.Cursor = None

    @staticmethod
    def initialize(db_path: str = "library_db"):
        Database.DB = sql.connect(db_path)
        Database.DB.execute("PRAGMA foreign_keys = 1")
        Database.CUR = Database.DB.cursor()
        Database.validate()

    @staticmethod
    def validate() -> None:
        if not Database.fetch_all_tables():
            Database.add_schema()
        else:
            print("[DB] Everything OK and READY.")

    @staticmethod
    def add_schema(path: str = "schema.sql") -> None:
        with open(path) as f:
            Database.DB.executescript(f.read())

    @staticmethod
    def add_row(row: dict) -> None:
        qstn_marks = []
        attrs = []
        vals = []
        for v, k in row.items():
            table_name, items = v, k
        for k, v in items.items():
            qstn_marks.append("?")
            attrs.append(k)
            vals.append(v)
        attrs = ", ".join(attrs)
        qstn_marks = ", ".join(qstn_marks)
        sql = f"INSERT INTO {table_name} ({attrs}) VALUES ({qstn_marks})"
        Database.CUR.execute(sql, vals)
        Database.DB.commit()

    @staticmethod
    def update(id: int, row: dict) -> None:
        for k, v in row.items():
            table_name, items = k, v
        attrs = ["%s =:%s" % (k, k) for k in items]
        attrs = ", ".join(attrs)
        sql = f"UPDATE {table_name} SET {attrs} WHERE id =:id"
        Database.CUR.execute(sql, items)
        Database.DB.commit()

    @staticmethod
    def delete(table_name: str, id: str) -> None:
        Database.CUR.execute(f"DELETE FROM {table_name} WHERE id = ?", (str(id),))
        Database.DB.commit()

    @staticmethod
    def fetch_table(table_name: str) -> list:
        Database.CUR.execute(f"SELECT * FROM {table_name}")
        return Database.CUR.fetchall()

    @staticmethod
    def fetch_all_tables() -> list:
        cursor = Database.CUR.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE'sqlite_%'"
        )
        return [table_title[0] for table_title in cursor]

    @staticmethod
    def fetch_columns(table: str) -> list:
        return [
            column[1] for column in Database.DB.execute(f"PRAGMA table_info({table})")
        ]

    @staticmethod
    def search_table(table_name: str, id: str):
        Database.CUR.execute(f"SELECT * FROM {table_name} WHERE  id = ?", (str(id),))
        return Database.CUR.fetchall()

    @staticmethod
    def reset_database(path: str = "library_db") -> None:
        if os.path.exists(path):
            os.remove(path)
        open(path, "w").close()
