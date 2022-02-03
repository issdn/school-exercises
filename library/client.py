import sqlite3
from tkinter import (
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
    Tk,
    Toplevel,
    mainloop,
)
from tkinter.ttk import Treeview
from database import OnEmptyError, DateError

SPECIAL_COLUMNS = ["id", "created_at", "end_period"]


class Window(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

    def close(self) -> None:
        self.destroy()


class ErrorWindow(Window):
    def __init__(self, err_msg: str, *args, **kwargs) -> None:
        Window.__init__(self, *args, **kwargs)
        self.title("Error")
        self.err_msg: str = err_msg
        self.build_error_window()

    def build_error_window(self):
        frame = Frame(master=self)
        error_message = Label(master=frame, text=self.err_msg)
        button = Button(master=frame, text="ok", command=lambda: self.close())
        error_message.pack()
        button.pack()
        frame.pack()


class SuperTree(Treeview):
    """
    Extended Treeview.
    """

    def __init__(self, database: object, table_name: str, *args, **kwargs):
        Treeview.__init__(self, *args, **kwargs)
        self.db: object = database
        self.table_name: str = table_name

    """
        Delete all treeview children and then rebuild it with updated database.
    """

    def reload(self) -> None:
        for child in self.get_children():
            self.delete(child)
        for column in self["columns"]:
            self.heading(column, text=column.upper(), anchor=CENTER)
        for row in self.db.fetch_table(self.table_name):
            self.insert("", END, values=row)
        print(f"Reloaded table {self.table_name}!")


class AddWindow(Window):
    """
    Take instance of treeview (one db table), name of the table and columns
    and build an winow to add an item to specified by "table_name" table.
    """

    def __init__(
        self,
        database: object,
        treeview: SuperTree,
        table_name: str,
        columns: list,
        *args,
        **kwargs,
    ) -> None:
        Window.__init__(self, *args, **kwargs)
        self.db: object = database
        self.tv: SuperTree = treeview
        self.table_name: str = table_name
        self.columns: list = columns
        self.build_window()

    """
        Build an *add to db* window, 
        disable id and created_at entries. 
    """

    def build_window(self) -> None:
        frame = Frame(master=self)
        entries = [Entry(master=frame) for _ in range(len(self.columns))]
        frame_buttons = Frame(master=frame)
        for column_nr, column in enumerate(self.columns):
            lbl_column = Label(master=frame, text=column.upper())
            entry = entries[column_nr]
            self.fill_entries(entry, column_nr)
            if column == "id" or column == "created_at":
                entry.config(state="disabled")
            lbl_column.pack(side=TOP)
            entry.pack(side=TOP)
        btn_save = Button(
            master=frame_buttons, text="Save", command=lambda: self.save(entries)
        )
        btn_cancel = Button(
            master=frame_buttons, text="Cancel", command=lambda: self.close()
        )
        btn_save.pack(side=LEFT)
        btn_cancel.pack(side=LEFT)
        frame_buttons.pack(side=TOP, pady=5)
        frame.pack()

    """
        Placeholder for filling entries in EditWindow.
    """

    def fill_entries(self, entry: object, column: int) -> None:
        ...  # <----- Black formatter does this, no idea why.

    """
        Get values from enteries, put them in a dictionary, 
        call database.add_row and reload whole tree.
    """

    def save(self, entries: list) -> None:
        """
        Slice off id and created_at and make insert.
        """
        values = [val.get() for val in entries]
        row = {col: values[col_nr] for col_nr, col in enumerate(self.columns)}
        row = self.validate_special_columns(row)
        try:
            self.db.add_row(table_name=self.table_name, row=row)
            self.tv.reload()
            self.close()
        except (OnEmptyError, DateError) as err:
            ErrorWindow(err_msg=err)

    def validate_special_columns(self, row: dict) -> None:
        """
        This checks if a value from special column like id or end_period is empty,
        if is, this func deletes it from the *row* payload so that sql can overwrite it with a default value.
        E.g -> created_at is empty -> this removes it from payload -> sql has no argument so it overwrites it with default value CURRENT_DATE.
        """
        to_delete = []
        for col in SPECIAL_COLUMNS:
            for k, v in row.items():
                if col == k and not v:
                    to_delete.append(k)
        for i in to_delete:
            del row[i]
        return row


class EditWindow(AddWindow):
    def __init__(self, item_id: int, row: list, *args, **kwargs) -> None:
        self.item_id: int = item_id
        self.row: list = row
        AddWindow.__init__(*args, **kwargs)

    def fill_entries(self, entry, column_nr) -> None:
        entry.insert(END, self.row[column_nr])

    def save(self, entries: list) -> None:
        values = [val.get() for val in entries]
        row = {
            column: values[column_nr] for column_nr, column in enumerate(self.columns)
        }
        row = self.validate_special_columns(row)
        try:
            self.db.update(table_name=self.table_name, row=row)
            print(f"Added row: {row} to table {self.table_name}")
            self.tv.reload()
        finally:
            self.close()


class Table(Frame):
    def __init__(self, name: str, database: object) -> None:
        Frame.__init__(self)
        self.name: str = name
        self.db: object = database
        self.label: Label = Label(master=self, text=self.name.upper()).pack()
        self.tv: SuperTree = SuperTree(
            master=self, database=self.db, table_name=self.name
        )
        self.tv.bind("<Button-3>", self.do_popup)
        self.columns: list[str] = self.db.fetch_columns(table=self.name)
        self.build_table()

    def build_table(self) -> None:
        self.tv["columns"] = self.columns
        self.tv.column("#0", anchor=W, width=0, stretch=False)
        self.tv.heading("#0", text="", anchor=W)
        for column in self.tv["columns"]:
            self.tv.column(column, anchor=CENTER, width=110, stretch=False)
            self.tv.heading(column, text=column.upper(), anchor=CENTER)
        for row in self.db.fetch_table(self.name):
            self.tv.insert("", END, values=row)

        self.tv.pack(side=TOP)
        btn_add_book = Button(
            master=self,
            text="ADD " + self.name.upper(),
            cursor="hand2",
            command=lambda: AddWindow(self.db, self.tv, self.name, self.columns),
        )
        btn_add_book.pack(side=BOTTOM, fill="both")
        self.pack(side=LEFT)

    def do_popup(self, event):
        menu = Menu(self, tearoff=0)
        item = self.tv.identify_row(event.y)
        row = self.tv.item(item)["values"]
        menu.add_command(label="Delete", command=lambda: self.delete(row[0]))
        menu.add_command(
            label="Edit",
            command=lambda: EditWindow(
                database=self.db,
                treeview=self.tv,
                table_name=self.name,
                item_id=item,
                row=row,
                columns=self.columns,
            ),
        )
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            pass

    def delete(self, id: int) -> None:
        self.db.delete(self.name, id)
        self.tv.reload()
        print(f"Deleted row with id {id} from table {self.name}!")


class Client(Tk):
    def __init__(self, database: object) -> None:
        Tk.__init__(self)
        self.db: object = database
        self.table_names: list[str] = self.db.fetch_all_tables()
        self.tables = []
        self.title("Library")
        self.resizable(False, True)
        self.build_client()
        self.mainloop()

    def build_client(self) -> None:
        self.tables = {
            table_name: Table(database=self.db, name=table_name)
            for table_name in self.table_names
        }
