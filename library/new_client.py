from tkinter import Tk, Frame, Label, Button, Menu, Entry, W, TOP, CENTER, LEFT, END, Tk, Toplevel, mainloop
from tkinter.ttk import Treeview
from database import Database

class AddWindow(Toplevel):
    def __init__(self, database: object, treeview: Treeview, table_name: str, columns: list) -> None:
        Toplevel.__init__(self)
        self.db: object = database
        self.tv: Treeview = treeview
        self.table_name: str = table_name
        self.columns: list = columns
        self.build_window()

    def build_window(self) -> None:
        frame = Frame(master=self)
        entries = [Entry(master=frame) for _ in range(len(self.columns))]
        frame_buttons = Frame(master=frame)
        for column in range(len(self.columns)):
            lbl_column = Label(master=frame, text=self.columns[column])
            entry = entries[column]
            entry.insert(END, self.row[column])
            lbl_column.pack(side=TOP)
            entry.pack(side=TOP)
        btn_save = Button(master=frame_buttons, text="Save", command = lambda: self.save(entries))
        btn_cancel = Button(master=frame_buttons, text="Cancel", command = lambda: self.close())
        btn_save.pack(side=LEFT)
        btn_cancel.pack(side=LEFT)
        frame_buttons.pack(side=TOP, pady=5)
        frame.pack()

    def save(self, entries: list) -> None:
        values = [val.get() for val in entries]
        row = {self.columns[column] : values[column] for column in range(len(self.columns))}
        try:
            self.tv.item(self.item_id, values=values)
            self.db.update(table_name = self.table_name, row=row)
        finally:
            self.close()

    def close(self) -> None:
        self.destroy()

class EditWindow(AddWindow):
    def __init__(self, item_id: int, row: list, *arg, **kw) -> None:
        self.item_id: int = item_id
        self.row: list = row
        super().__init__(*arg, **kw)

    def build_window(self) -> None:
        frame = Frame(master=self)
        entries = [Entry(master=frame) for _ in range(len(self.columns))]
        frame_buttons = Frame(master=frame)
        for column in range(len(self.columns)):
            lbl_column = Label(master=frame, text=self.columns[column])
            entry = entries[column]
            entry.insert(END, self.row[column])
            lbl_column.pack(side=TOP)
            entry.pack(side=TOP)
        btn_save = Button(master=frame_buttons, text="Save", command = lambda: self.save(entries))
        btn_cancel = Button(master=frame_buttons, text="Cancel", command = lambda: self.close())
        btn_save.pack(side=LEFT)
        btn_cancel.pack(side=LEFT)
        frame_buttons.pack(side=TOP, pady=5)
        frame.pack()

    def save(self, entries: list) -> None:
        values = [val.get() for val in entries]
        row = {self.columns[column] : values[column] for column in range(len(self.columns))}
        try:
            self.tv.item(self.item_id, values=values)
            self.db.update(table_name = self.table_name, row=row)
        finally:
            self.close()

    def close(self) -> None:
        self.destroy()

class Table(Frame):
    def __init__(self, name: str, database: object):
        Frame.__init__(self)
        self.name: str = name
        self.db: object = database
        self.label: Label = Label(master = self, text = self.name.upper()).pack()
        self.tv: Treeview = Treeview(master = self)
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

        self.tv.pack(side=LEFT)
        self.pack(side=LEFT)
    
    def do_popup(self, event):
        menu = Menu(self, tearoff=0)
        item = self.tv.identify_row(event.y)
        row = self.tv.item(item)["values"]
        menu.add_command(label="Delete", command = lambda: self.delete(item))
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
            menu.grab_release()
        
    def delete(self, item: int) -> None:
        self.tv.delete(item)

class Client(Tk):
    def __init__(self, database: object):
        Tk.__init__(self)
        self.db: object = database
        self.table_names: list[str] = self.db.fetch_all_tables()
        self.tables = []
        self.title("Library")
        self.build_client()
        self.mainloop()

    def build_client(self):
        self.tables = [Table(database = self.db, name = table_name) for table_name in self.table_names]

        # btn_add_book = Button(   
        #                         master=self, 
        #                         text="ADD BOOK", 
        #                         cursor = "hand2", 
        #                         command = lambda: AddWindow(   
        #                                                     tables["books"].table_name, 
        #                                                     self.database, 
        #                                                     tables["books"].treeview
        #                                                     )
        #                         )
        # btn_add_user = Button(master=self, text="ADD USER", cursor = "hand2")
        # btn_borrow = Button(master=self, text="BORROW", cursor = "hand2")