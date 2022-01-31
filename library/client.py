import tkinter as tk
from tkinter import ttk
from database import Database

class Subwindow(tk.Toplevel):
    def __init__(self, table_name: str, database: object, treeview: object, *ar, **kw) -> None:
        super().__init__(*ar, *kw)
        self.table_name: str = table_name
        self.db: object = database
        self.columns: list = self.db.fetch_values(table_name)
        self.tv: object = treeview
        self.build_subwindow()

    def build_subwindow(self) -> None:
        main_frame = tk.Frame(master=self)
        entries = [tk.Entry(master=main_frame) for _ in range(len(self.columns))]
        frm_button = tk.Frame(master=main_frame)
        for column in range(len(self.columns)):
            lbl_column = tk.Label(master=main_frame, text=self.columns[column])
            lbl_entry = entries[column]
            lbl_column.pack(side=tk.TOP)
            lbl_entry.pack(side=tk.TOP)
        btn_save = tk.Button(master=frm_button, text="Save", command = lambda: self.save(entries))
        btn_cancel = tk.Button(master=frm_button, text="Cancel", command = lambda: self.close())
        btn_save.pack(side=tk.LEFT)
        btn_cancel.pack(side=tk.LEFT)
        frm_button.pack(side=tk.TOP, pady=5)
        main_frame.pack()

    def close(self) -> None:
        self.destroy()
    
    def save(self, entries: list) -> None:
        values = [val.get() for val in entries]
        row = {self.columns[column] : values[column] for column in range(len(self.columns))}
        try:
            self.treeview.insert(parent="", text="", values=values)
            self.db.add_row(table_name = self.table_name, row=row)
        finally:
            self.close()

class EditSubwindow(Subwindow):
    def __init__(self, item_id: int, values: list, *ar, **kw) -> None:
        self.item_id: int = item_id 
        self.values: list = values
        super().__init__(*ar, *kw)

    def build_subwindow(self) -> None:
        main_frame = tk.Frame(master=self)
        entries = [tk.Entry(master=main_frame) for _ in range(len(self.columns))]
        frm_button = tk.Frame(master=main_frame)
        for column in range(len(self.columns)):
            lbl_column = tk.Label(master=main_frame, text=self.columns[column])
            lbl_entry = entries[column]
            lbl_entry.insert('end', self.values[column])
            lbl_column.pack(side=tk.TOP)
            lbl_entry.pack(side=tk.TOP)
        btn_save = tk.Button(master=frm_button, text="Save", command = lambda: self.save(entries))
        btn_cancel = tk.Button(master=frm_button, text="Cancel", command = lambda: self.close())
        btn_save.pack(side=tk.LEFT)
        btn_cancel.pack(side=tk.LEFT)
        frm_button.pack(side=tk.TOP, pady=5)
        main_frame.pack()

    def save(self, entries: list) -> None:
        vals = [val.get() for val in entries]
        row = {self.columns[column] : vals[column] for column in range(len(self.columns))}
        try:
            self.tv.item(self.item_id, values=vals)
            self.db.update(table_name = self.table_name, row=row)
        finally:
            self.close()

class TableGUI():
    def __init__(self, database: object, table_name: str):
        self.database: object = database
        self.table_name: str = table_name
        self.table_frm: object = tk.Frame()
        self.treeview: object = ttk.Treeview(master=self.table_frm)
        self.table_columns: list[tuple(str)] = self.database.fetch_values(table_name)
        self.init_table()
    
    def init_table(self) -> None:
        self.treeview.bind('<Button-3>', self.do_popup)
        # self.treeview.bind('<ButtonRelease-1>', self.selectItem)
        lbl_table_title = tk.Label(master=self.table_frm, text=self.table_name.upper())
        self.treeview["columns"] = self.table_columns
        self.treeview.column('#0', anchor=tk.W, width=0, stretch=False)
        self.treeview.heading('#0', text='', anchor=tk.W)
        for column in self.treeview["columns"]:
            self.treeview.column(column, anchor=tk.CENTER, width=110, stretch=False)
            self.treeview.heading(column, text=column.upper(), anchor=tk.CENTER)
            index = 0
            for values in self.database.fetch_table(self.table_name):
                self.treeview.insert(parent="", index=index, text="", values=values)
                index += 1

        lbl_table_title.pack()
        self.treeview.pack(side=tk.LEFT)
        self.table_frm.pack(side=tk.LEFT)
    
    def do_popup(self, event):
        menu = tk.Menu(self.table_frm, tearoff=0)
        item = self.treeview.identify_row(event.y)
        item_values = self.treeview.item(item)["values"]
        menu.add_command(label="Delete", command = lambda: self.delete(item))
        menu.add_command(label="Edit", command = lambda: EditSubwindow  ( 
                                                                        table_name = self.table_name, 
                                                                        item_id = item,
                                                                        values = item_values, 
                                                                        treeview = self.treeview, 
                                                                        database = self.database
                                                                        )
                        )
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def delete(self, item: int) -> None:
        self.tv.delete(item)

class Client():
    def __init__(self, database: object) -> None:
        self.database: object = database
        self.window = tk.Tk()
        self.window.title("Library")
        self.build_database()
        self.window.mainloop()

    def build_database(self) -> None:
        global_table_titles = []
        [global_table_titles.append(table_title[0]) for table_title in self.database.fetch_all_tables()]

        tables = {g_table_title: TableGUI(database = self.database, table_name = g_table_title) for g_table_title in global_table_titles}

        btn_frm = tk.Frame(master=self.window)
        btn_add_book = tk.Button(   
                                master=btn_frm, 
                                text="ADD BOOK", 
                                cursor = "hand2", 
                                command = lambda: Subwindow(   
                                                            tables["books"].table_name, 
                                                            self.database, 
                                                            tables["books"].treeview
                                                            )
                                )
        btn_add_user = tk.Button(master=btn_frm, text="ADD USER", cursor = "hand2")
        btn_borrow = tk.Button(master=btn_frm, text="BORROW", cursor = "hand2")

        btn_add_book.pack(side=tk.TOP, fill=tk.BOTH)
        btn_add_user.pack(side=tk.TOP, fill=tk.BOTH)
        btn_borrow.pack(side=tk.TOP, fill=tk.BOTH)
        btn_frm.pack(side=tk.LEFT)

    def delete(self):
        print(self.selected_item)


def main():
    pass
    # database.add_books("Mandragora", "Witcher", "Potter")
    # database.add_users({"John", "Walker"}, {"Milker", "Dilker"}, {"Karol", "Bielski"})
    # database.borrow(1, 1)

if __name__ == "__main__":
    main()