import sqlite3 as sql
import os


class Datenbank:
    DB: sql.Connection = None
    CUR: sql.Cursor = None

    @staticmethod
    def initialize(path: str = "cd_datenbank.db"):
        # Datenbank Datei erstellen wenn nicht existiert.
        if not os.path.exists(path):
            open(path, "w").close()
        # Verbindung und Cursor setzen.
        Datenbank.DB = sql.connect(path)
        Datenbank.CUR = Datenbank.DB.cursor()
        # Schema anlegen wenn cds Tabelle nicht existiert.
        if not Datenbank.CUR.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='cds'; """
        ).fetchall():
            with open("schema.sql") as f:
                Datenbank.DB.executescript(f.read())


class CD:
    def __init__(self, interpret: str, titel: str, abspielzeit: str) -> None:
        self.interpret: str = interpret
        self.titel: str = titel
        self.abspielzeit: str = abspielzeit

    def __repr__(self) -> str:
        return "%s,%s,%s\n" % (
            self.interpret,
            self.titel,
            self.abspielzeit,
        )

    def __str__(self) -> str:
        return "CD: | Interpet: %s, Titel: %s, Abspielzeit: %s |" % (
            self.interpret,
            self.titel,
            self.abspielzeit,
        )

    def vals(self) -> list:
        return [self.interpret, self.titel, self.abspielzeit]


class Verwaltung:
    def add(self, cd: CD) -> None:
        Datenbank.CUR.execute(
            "INSERT INTO cds (interpret, titel, abspielzeit) VALUES (?, ?, ?)",
            (
                cd.interpret,
                cd.titel,
                cd.abspielzeit,
            ),
        )
        Datenbank.DB.commit()

    def find_titel(self, titel: str) -> object:
        Datenbank.CUR.execute("SELECT * FROM cds WHERE titel = ?", (titel,))
        return Datenbank.CUR.fetchall()

    def get_all(self) -> object:
        Datenbank.CUR.execute("SELECT * FROM cds")
        fetch = Datenbank.CUR.fetchall()
        return [CD(item[0], item[1], item[2]) for item in fetch]

    def delete_cd(self, titel) -> None:
        Datenbank.CUR.execute("DELETE FROM cds WHERE titel = ?", (titel,))
        Datenbank.DB.commit()

    def to_string(self) -> None:
        ...

    def find_interpret(self, interpret: str) -> None:
        ...

    def sort_titel(self) -> None:
        ...

    def sort_interpret(self) -> None:
        ...

    def next(self) -> None:
        ...

    def first(self) -> None:
        ...

    def get_cd(self) -> CD:
        ...


if __name__ == "__main__":
    # Datenbank.erstellen()
    Datenbank.initialize()
    verv = Verwaltung()
    print(verv.get_all())
