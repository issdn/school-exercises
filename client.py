from tkinter import BOTTOM, Tk, Frame, Label, Button, Menu, Entry, W, TOP, CENTER, LEFT, END, Tk, Toplevel, mainloop
from tkinter.ttk import Treeview

class SuperTree(Treeview):
    """
        Extended Treeview.
    """
    def __init__(self, database: object, table_name: str, *ar, **kw):
        Treeview.__init__(self, *ar, **kw)
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
            self.insert('', END, values = row)
        print(f"Reloaded table {self.table_name}!")

class AddWindow(Toplevel):
    """
        Take instance of treeview (one db table), name of the table and columns 
        and build an winow to add an item to specified by "table_name" table. 
    """
    def __init__(self, database: object, treeview: SuperTree, table_name: str, columns: list) -> None:
        Toplevel.__init__(self)
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
        for column in range(len(self.columns)):
            lbl_column = Label(master=frame, text=self.columns[column].upper())
            entry = entries[column]
            self.fill_entries(entry, column)
            if self.columns[column] == "id" or self.columns[column] == "created_at":
                entry.config(state = "disabled")
            lbl_column.pack(side=TOP)
            entry.pack(side=TOP)
        btn_save = Button(master=frame_buttons, text="Save", command = lambda: self.save(entries))
        btn_cancel = Button(master=frame_buttons, text="Cancel", command = lambda: self.close())
        btn_save.pack(side=LEFT)
        btn_cancel.pack(side=LEFT)
        frame_buttons.pack(side=TOP, pady=5)
        frame.pack()

    """
        Placeholder for filling entries in EditWindow.
    """
    def fill_entries(self, entry: object, column: int) -> None: ...

    """
        Get values from enteries, put them in a dictionary, 
        call database.add_row and reload whole tree.
    """
    def save(self, entries: list) -> None:
        values = [val.get() for val in entries]
        row = {self.columns[column] : values[column] for column in range(len(self.columns))}
        try:    
            self.db.add_row(table_name = self.table_name, row=row)
            self.tv.reload()
        finally:
            self.close()

    def close(self) -> None:
        self.destroy()

class EditWindow(AddWindow):
    def __init__(self, item_id: int, row: list, *arg, **kw) -> None:
        self.item_id: int = item_id
        self.row: list = row
        super().__init__(*arg, **kw)

    def fill_entries(self, entry, column) -> None:
        entry.insert(END, self.row[column])

    def save(self, entries: list) -> None:
        values = [val.get() for val in entries]
        row = {self.columns[column] : values[column] for column in range(len(self.columns))}
        try:
            self.db.update(table_name = self.table_name, row=row)
            print(f"Added row: {row} to table {self.table_name}")
            self.tv.reload()
        finally:
            self.close()

    def close(self) -> None:
        self.destroy()

class Table(Frame):
    def __init__(self, name: str, database: object) -> None:
        Frame.__init__(self)
        self.name: str = name
        self.db: object = database
        self.label: Label = Label(master = self, text = self.name.upper()).pack()
        self.tv: SuperTree = SuperTree(master = self, database = self.db, table_name = self.name)
        self.tv.bind('<Button-3>', self.do_popup)
        self.columns: list[str] = self.db.fetch_columns(table = self.name)
        self.build_table()
    
    def build_table(self) -> None:
        self.tv["columns"] = self.columns
        self.tv.column('#0', anchor=W, width=0, stretch=False)
        self.tv.heading('#0', text='', anchor=W)
        for column in self.tv["columns"]:
            self.tv.column(column, anchor=CENTER, width=110, stretch=False)
            self.tv.heading(column, text=column.upper(), anchor=CENTER)
        for row in self.db.fetch_table(self.name):
            self.tv.insert('', END, values=row)

        self.tv.pack(side=TOP)
        btn_add_book = Button(   
                                master = self, 
                                text = "ADD " + self.name.upper(), 
                                cursor = "hand2", 
                                command = lambda: AddWindow(self.db, 
                                                            self.tv,
                                                            self.name, 
                                                            self.columns))
        btn_add_book.pack(side = BOTTOM, fill = "both")
        self.pack(side=LEFT)
    
    def do_popup(self, event):
        menu = Menu(self, tearoff=0)
        item = self.tv.identify_row(event.y)
        row = self.tv.item(item)["values"]
        menu.add_command(label="Delete", command = lambda: self.delete(row[0]))
        menu.add_command(   label="Edit", 
                            command = lambda: EditWindow(   database = self.db, 
                                                            treeview = self.tv, 
                                                            table_name = self.name, 
                                                            item_id = item, 
                                                            row = row, 
                                                            columns = self.columns))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            pass
        
    def delete(self, id: int) -> None:
        # self.tv.delete(item)
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
        self.tables = {table_name : Table(database = self.db, name = table_name) for table_name in self.table_names}
                            