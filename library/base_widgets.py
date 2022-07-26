from typing import Tuple
from config import Config
from database import Database
from tkinter import (
    Grid,
    Tk,
    Frame,
    Label,
    Button,
    Menu,
    Entry,
    W,
    TOP,
    CENTER,
    BOTTOM,
    LEFT,
    END,
    BOTH,
    Tk,
    Toplevel,
    mainloop,
    messagebox,
)
from tkinter.ttk import Treeview
from bibliothek_types import *
from validator import Validator
from utils import DictManipulator as Mp

"""
    Bases for the widgets. To edit the actual gui go to client.py
"""


class SuperTree(Treeview):
    def __init__(self, db_table_name: str, columns: list, *args, **kwargs):
        Treeview.__init__(self, *args, **kwargs)
        self.db_table_name: str = db_table_name
        self.columns: list = columns
        self.db_columns: list = Database.fetch_columns(self.db_table_name)

    def fill(self, db_columns: list) -> None:
        self.column("#0", anchor=W, width=0, stretch=False)
        self.heading("#0", text="", anchor=W)
        self["columns"] = db_columns
        for column in self.columns:
            self.column(column, anchor=CENTER, width=110)
            self.heading(column, text=column.upper(), anchor=CENTER)
        for row in Database.fetch_table(self.db_table_name):
            self.insert("", END, values=row)

    def reload(self) -> None:
        """
        Delete all treeview children and then rebuild it with updated database.
        """
        for child in self.get_children():
            self.delete(child)
        for column in self.db_columns:
            self.heading(column, text=column.upper(), anchor=CENTER)
        for row in Database.fetch_table(self.db_table_name):
            self.insert("", END, values=row)


class Window(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

    def close(self) -> None:
        self.destroy()


class LabelEntryFrame(Frame):
    def __init__(self, row: RowT, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.row: RowT = row
        self.entries: list[Entry] = None

    def build(self):
        for k, v in self.row.items():
            lbl = Label(master=self, text=k)
            etr = SuperEntry(master=self)
            etr.insert(END, v)
            self.entries.append(etr)
            lbl.pack(side=TOP)
            etr.pack(side=TOP)

    def entry_values(self) -> RowT:
        return {self.row[nr]: e.get() for nr, e in enumerate(self.entries)}


class SuperEntry(Entry):
    def __init__(self, db_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.db_name: str = db_name

    def get(self) -> Tuple[str, str]:
        """Return the text."""
        inside_value = self.tk.call(self._w, "get")
        return self.db_name, inside_value


class AddWindow(Window):
    """
    Take instance of treeview (one db table), name of the table and columns
    and build an winow to add an item to specified by "table_name" table.
    """

    def __init__(
        self,
        treeview: SuperTree,
        table_name: str,
        row: RowT,
        *args,
        **kwargs,
    ) -> None:
        Window.__init__(self, *args, **kwargs)
        self.geometry("250x150")
        self.tv: SuperTree = treeview
        self.table_name: str = table_name
        self.row: RowT = row
        self.build_window()

    """
        Build an *add to db* window, 
        disable id and created_at entries. 
    """

    def build_window(self) -> None:
        frame = Frame(master=self)
        frame_buttons = Frame(master=frame)
        inner_window = LabelEntryFrame(row=self.row)
        inner_window.build()
        btn_save = Button(
            master=frame_buttons,
            text="Save",
            command=lambda: self.save(inner_window.entry_values()),
        )
        btn_cancel = Button(
            master=frame_buttons, text="Cancel", command=lambda: self.close()
        )
        btn_save.pack(side=LEFT)
        btn_cancel.pack(side=LEFT)
        frame_buttons.pack(side=TOP, pady=5)
        frame.pack()

    def save(self, row: RowT) -> None:
        """
        Takes data from entries and saves them in database.
        """
        v = Validator(row)
        v.validate()
        e = v.errors
        if e:
            messagebox.showerror("Error", e[0], parent=self)
        else:
            Database.add_row(v.normalized())
            self.tv.reload()
            self.close()


class EditWindow(AddWindow):
    def __init__(self, *args, **kwargs) -> None:
        AddWindow.__init__(self, *args, **kwargs)

    def save(self, entries: list) -> None:
        values = [val.get() for val in entries]
        row = {
            self.table_name: {
                col: values[col_nr] for col_nr, col in enumerate(self.db_columns)
            }
        }
        v = Validator(row, True)
        v.validate()
        e = v.errors
        if e:
            messagebox.showerror("Error", e[0], parent=self)
        else:
            Database.update(row[self.table_name]["id"], v.normalized())
            self.tv.reload()
            self.close()


class Table(Frame):
    def __init__(
        self, name: str, db_name: str, column_names: list, *args, **kwargs
    ) -> None:
        Frame.__init__(self, *args, **kwargs)
        self.name: str = name
        self.db_name: str = db_name
        self.column_names: list = column_names
        self.label: Label = Label(master=self, text=self.name.upper()).pack()
        # self.tv.bind("<Button-3>", self.do_popup)
        self.db_columns: list[str] = Database.fetch_columns(table=self.name)
        self.tv: SuperTree = SuperTree(
            master=self, db_table_name=self.name, columns=self.column_names
        )
        self.tv.pack(side=TOP, fill=BOTH, expand=1)
        self.build_table()
        self.pack(side=LEFT, fill=BOTH, expand=1)

    def build_table(self) -> None:
        ...

    def add(self):
        entries = {c: "" for c in self.db_columns}
        AddWindow(self.tv, self.name, self.column_names, entries)

    def edit(self):
        try:
            item = self.tv.selection()[0]
            row = dict(zip(self.column_names, self.tv.item(item)["values"]))
            EditWindow(
                treeview=self.tv,
                table_name=self.name,
                item_id=item,
                row=row,
                columns=self.column_names,
                db_columns=self.db_columns,
            )
        except IndexError:
            messagebox.showerror("Error", "You must select an item first!")

    def delete(self, id: int) -> None:
        Database.delete(self.name, id)
        self.tv.reload()
