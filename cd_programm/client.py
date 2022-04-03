from main import *
from tkinter import (
    Button,
    Tk,
    Frame,
    Toplevel,
    Label,
    Entry,
    CENTER,
    END,
    W,
    messagebox,
)
from tkinter.ttk import Treeview


class Table(Treeview):
    def __init__(self, verv: Verwaltung, *args, **kwargs) -> None:
        Treeview.__init__(self, *args, **kwargs)
        self.verv: Verwaltung = verv

    def build(self):
        self.column("#0", anchor=W, width=0, stretch=False)
        self.heading("#0", text="", anchor=W)
        self["columns"] = ("Interpret", "Titel", "Abspielzeit")
        for column in self["columns"]:
            self.column(column, anchor=CENTER, width=110)
            self.heading(column, text=column.upper(), anchor=CENTER)
        self.insert_rows()

    def reload(self) -> None:
        for child in self.get_children():
            self.delete(child)
        self.insert_rows()

    def delete_item(self) -> None:
        try:
            selected_item = self.selection()[0]
            values = self.item(selected_item)["values"]
            self.delete(selected_item)
            self.verv.delete_cd(values[0])
        except IndexError:
            messagebox.showerror("Error", "Erst eine CD selektieren!")

    def insert_rows(self):
        for row in self.verv.get_all():
            self.insert("", END, values=row.vals())


class AddWindow(Toplevel):
    def __init__(self, verv: Verwaltung, tb: Table, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry("200x200")
        self.verv: Verwaltung = verv
        self.tb: Table = tb
        self.build()

    def build(self):
        frame = Frame(master=self)

        lbl_interpret = Label(master=frame, text="Interpret")
        lbl_interpret.pack()
        ntr_interpret = Entry(master=frame)
        ntr_interpret.pack()

        lbl_titel = Label(master=frame, text="Titel")
        lbl_titel.pack()
        ntr_titel = Entry(master=frame)
        ntr_titel.pack()

        lbl_abspielzeit = Label(master=frame, text="Abspielzeit")
        lbl_abspielzeit.pack()
        ntr_abspielzeit = Entry(master=frame)
        ntr_abspielzeit.pack()

        btn_add = Button(
            master=frame,
            text="ADD",
            command=lambda: self.save(
                (ntr_interpret.get(), ntr_titel.get(), ntr_abspielzeit.get())
            ),
        )
        btn_add.pack(pady=10, fill="x")

        frame.pack()

    def save(self, entries: tuple[Entry]) -> None:
        interpret, titel, abspielzeit = entries
        cd = CD(interpret, titel, float(abspielzeit))
        self.verv.add(cd)
        self.tb.reload()
        self.destroy()


class Main(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.verv = Verwaltung()
        Datenbank.initialize()
        self.build()

    def build(self):
        frame = Frame(master=self, pady=25)
        lbl_cd = Label(master=self, text="CD Datenbank", pady=10)
        lbl_cd.pack()
        table = Table(master=self, verv=self.verv)
        table.build()
        table.pack()
        btn_add = Button(
            master=frame,
            text="Add CD",
            width=15,
            command=lambda: AddWindow(verv=self.verv, tb=table),
        )
        btn_add.pack(fill="x")
        btn_del = Button(
            master=frame, text="Delete CD", width=15, command=table.delete_item
        )
        btn_del.pack(fill="x")
        frame.pack()


if __name__ == "__main__":
    gui = Main()
    gui.mainloop()
