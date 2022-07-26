from database import Database
from tkinter import (
    Tk,
    Button,
    LEFT,
    BOTH,
    Tk,
)
from bibliothek_types import *
from validator import Validator
from utils import DictManipulator as Mp
from base_widgets import Table


class EntryError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message

    def __str__(self) -> str:
        return self.message


class BooksTable(Table):
    def __init__(self, name: str, db_name: str, *args, **kwargs) -> None:
        super().__init__(name, db_name, *args, **kwargs)

    def build_table(self) -> None:
        add_button = Button(
            master=self, text="Add", cursor="hand2", command=lambda: self.add()
        )
        delete_button = Button(master=self, text="Delete", cursor="hand2")
        edit_button = Button(
            master=self, text="Edit", cursor="hand2", command=lambda: self.edit()
        )
        borrow_button = Button(
            master=self, text="Borrow", cursor="hand2", command=lambda: self.borrow()
        )

        add_button.pack(side=LEFT, fill=BOTH, expand=1)
        edit_button.pack(side=LEFT, fill=BOTH, expand=1)
        delete_button.pack(side=LEFT, fill=BOTH, expand=1)
        borrow_button.pack(side=LEFT, fill=BOTH, expand=1)

    def borrow(self) -> None:
        item = self.tv.selection()[0]
        row = self.tv.item(item)["values"]


class UsersTable(Table):
    def __init__(self, name: str, db_name: str, *args, **kwargs) -> None:
        super().__init__(name, db_name, *args, **kwargs)

    def build_table(self) -> None:
        add_button = Button(
            master=self, text="Add", cursor="hand2", command=lambda: self.add()
        )
        delete_button = Button(master=self, text="Delete", cursor="hand2")
        edit_button = Button(master=self, text="Edit", cursor="hand2")

        add_button.pack(side=LEFT, fill=BOTH, expand=1)
        edit_button.pack(side=LEFT, fill=BOTH, expand=1)
        delete_button.pack(side=LEFT, fill=BOTH, expand=1)


class BorrowedTable(Table):
    def __init__(self, name: str, db_name: str, *args, **kwargs) -> None:
        super().__init__(name, db_name, *args, **kwargs)

    def build_table(self) -> None:
        return_button = Button(master=self, text="Return", cursor="hand2")

        return_button.pack(side=LEFT, fill=BOTH, expand=1)


class Client(Tk):
    def __init__(self) -> None:
        Tk.__init__(self)
        Database.initialize()
        self.table_names: list[str] = Database.fetch_all_tables()
        self.tables = []
        self.title("Library")
        # self.resizable(False, True)
        self.build_client()
        self.mainloop()

    def build_client(self) -> None:
        BooksTable("books", "books", ["id", "title"])
        UsersTable("users", "users", ["id", "name", "surname"])
        BorrowedTable(
            "borrowed",
            "borrowed",
            ["id", "borrowed_at", "book_id", "user_id", "end_date"],
        )
