import re
from bibliothek_types import *
from database import Database
from datetime import datetime
from utils import DM as DM


class DatabaseError(Exception):
    ...


class Validator:
    def __init__(self, row: RowT, require_id: bool = None) -> None:
        self.row: RowT = row
        self.require_id: bool = require_id
        self.errors: list = []

    def validate(self) -> None:
        if self.require_id:
            table_name = DM.first_key(self.row)
            idd = self.row[table_name].pop("id")
            self.id_in_database(table_name, idd)
        elif not self.require_id and "id" in DM.first_value(self.row):
            del DM.first_value(self.row)["id"]
        table = DM.first_key(self.row)
        if table == "books":
            self.validate_books()
        elif table == "users":
            self.validate_users()
        elif table == "borrowed":
            self.validate_borrowed()
        else:
            assert DatabaseError(
                "Table doesn't exist! Change config or contact the administrator!"
            )

    def validate_books(self) -> None:
        # gets value from row eg. {"books": {"title": "The Witcher"}} -> {"title": "The Witcher"}
        entries = DM.first_value(self.row)
        for k, v in entries.items():
            self.empty({k: v})

    def validate_users(self) -> None:
        # for eg. look validate_books
        entries = DM.first_value(self.row)
        for k, v in entries.items():
            self.regex("[^a-zA-Z0-9äöüÄÖÜß]", {k: v})
            self.empty({k: v})

    def validate_borrowed(self) -> None:
        end_date = self.row.pop["end_date"]
        for e in DM.first_value(self.row):
            self.id_in_database(DM.first_key(self.row), DM.first_value(e))
        self.check_date_format(end_date)

    def regex(self, regex: str, entry: dict | EntryT) -> None:
        ((k, v),) = entry.items()
        if not bool(re.match(regex, str(v))):
            self.errors.append(f"{k} entry has invalid characters.")

    def id_in_database(self, table_name: str, idd: int) -> None:
        if not Database.search_table(table_name, idd):
            self.errors.append(
                f"Item with id: {idd} doesn't exist in the table {table_name}!"
            )

    def integer(self, entry: EntryT) -> None:
        ((k, v),) = entry.items()
        try:
            int(v)
        except:
            self.errors.append(f"{k} must be of int type.")

    def check_date_format(self, date: str) -> None:
        try:
            year, month, day = date.split("-")
            check_date = datetime(int(year), int(month), int(day)).date()
        except:
            self.errors.append(
                f"Formate of the date is invalid! Valid Format: yyyy-mm-dd"
            )
        if datetime(2000, 1, 1).date() > check_date:
            self.errors.append(f"Date cannot be older than 2000-1-1")

    def empty(self, entry: dict | EntryT) -> None:
        ((k, v),) = entry.items()
        if not len(str(v)):
            self.errors.append(f"{k} cannot be empty.")
