import sqlite3 as sql
from datetime import datetime


class OnEmptyError(Exception):
    def __init__(self, field: str = None) -> None:
        self.field: str = field

    def __str__(self) -> str:
        return f"Field {self.field.upper()} cannot be empty!"


class DateError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message

    def __str__(self) -> str:
        return self.message


def check_if_empty(row: dict):
    for k, v in row.items():
        if not v:
            raise OnEmptyError(k)


def check_date_format(date: str):
    try:
        year, month, day = date.split("-")
        check_date = datetime(int(year), int(month), int(day)).date()
    except:
        raise DateError("Formate of the date is invalid! Valid Format: yyyy-mm-dd")
    if datetime(2000, 1, 1).date() > check_date:
        raise DateError("Date cannot be older than 2000-1-1")


class Database:
    def __init__(self, db_path: str = "library"):
        self.db: sql.Connection = sql.connect(db_path)
        self.db.execute("PRAGMA foreign_keys = 1")
        self.cur: sql.Cursor = self.db.cursor()

    def add_schema(self, path: str = "schema.sql") -> None:
        with open(path) as f:
            self.db.executescript(f.read())

    def add_row(self, table_name: str, row: dict) -> None:
        check_if_empty(row)
        if "end_period" in row:
            check_date_format(row["end_period"])
        qstn_marks = []
        attrs = []
        vals = []
        for k, v in row.items():
            qstn_marks.append("?")
            attrs.append(k)
            vals.append(v)
        attrs = ", ".join(attrs)
        qstn_marks = ", ".join(qstn_marks)
        sql = f"INSERT INTO {table_name} ({attrs}) VALUES ({qstn_marks})"
        print(sql, vals)
        self.cur.execute(sql, vals)
        self.db.commit()

    def update(self, table_name: str, row: dict) -> None:
        check_if_empty(row)
        if "end_period" in row:
            check_date_format(row["end_period"])
        attrs = ["%s =:%s" % (k, k) for k in row]
        attrs = ", ".join(attrs)
        sql = f"UPDATE {table_name} SET {attrs} WHERE id =:id"
        print(sql)
        self.cur.execute(sql, row)
        self.db.commit()

    def delete(self, table_name: str, id: str) -> None:
        self.cur.execute(f"DELETE FROM {table_name} WHERE id = ?", (str(id),))
        self.db.commit()

    def fetch_table(self, table_name: str) -> list:
        self.cur.execute(f"SELECT * FROM {table_name}")
        return self.cur.fetchall()

    def fetch_all_tables(self) -> list:
        cursor = self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE'sqlite_%'"
        )
        return [table_title[0] for table_title in cursor]

    def fetch_columns(self, table: str) -> list:
        return [column[1] for column in self.db.execute(f"PRAGMA table_info({table})")]

    def search_table(self, table_name: str, id: str):
        return self.cur.execute(f"SELECT * FROM {table_name} WHERE  id = ?", (str(id)))
