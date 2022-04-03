import os

""""
Mit den Funktionen, die Java zur Verarbeitung von Dateien mit wahlfreiem Zugriff zur Verfügung 
stellt, können Dateien beliebigen Inhalts untersucht werden, z.B. Word-Dokumente, Excel-Tabellen, 
mpeg-Filme oder MP3-Musik.
Wenn Sie einen üblichen MP3-Spieler verwenden, so wird meistens zu jedem Titel der Name des Titels, 
der Interpret usw. als Meta-Info angezeigt. Das funktioniert nur deshalb, weil diese Informationen in 
der mp3-Datei codiert sind.
Die Meta-Informationen einer mp3-Datei sind in den letzten 128 Byte – dem sog. ID3v1-Tag - einer 
Datei codiert und haben folgende Bedeutung:
    ID3v1-Tag
    Header 3 Byte=“TAG“ (ASCII)
    Title 30 Byte (ASCII)
    Artist 30 Byte (ASCII)
    Album 30 Byte (ASCII)
    Year 4 Byte (ASCII)
    Comment 30 Byte (ASCII)
    Genre 1 Byte (unknown=$FF)
Es soll eine Klasse zur komfortablen Verwaltung dieser TAGs entwickelt werden. 
Mindestanforderung:
- Einlesen und Speichern eines TAGs.
- Die Informationen aus einer solchen Struktur sollen auf dem Bildschirm ausgegeben 
bzw. über die Tastatur gesetzt werden können.
1. Beschreiben Sie die Klasse zunächst in UML.
2. Implementation und Testen.
3. Implementation weiterer Funktionen (Genre Klartextausgabe, Speicherung in Textdatei, …)
"""


class MaxBytesError(Exception):
    def __init__(self) -> None:
        super().__init__()


class Mp3Reader:
    def __init__(self, path: str = "m2.mp3") -> None:
        self.path: str = path
        self.tag_byte_start: int = self.tag_bytes()
        self.switch = {
            1: self.__title,
            2: self.__artist,
            3: self.__album,
            4: self.__year,
            5: self.__comment,
            6: self.__genre,
        }

    def tag_bytes(self) -> int:
        return os.path.getsize(self.path) - 125

    def read(self, item: int):
        with open(self.path, "rb") as f:
            print(self.switch[int(item)](f, "r"))

    def write(self, item: int, arg: str):
        with open(self.path, "wb") as f:
            self.switch[int(item)](f, "w", arg)

    def __title(self, f, fun_type, str_to_write: str = None):
        f.seek(self.tag_byte_start)
        if fun_type == "r":
            return f.read(30).decode("latin-1")
        try:
            arg = str_to_write.encode("utf-8")
            self.__is_right_size(arg, 30)
            f.write(arg)
        except MaxBytesError as e:
            print(e)

    def __artist(self, f, fun_type, str_to_write: str = None):
        f.seek(self.tag_byte_start + 30)
        if fun_type == "r":
            return f.read(30).decode("latin-1")
        try:
            arg = str_to_write.encode("utf-8")
            self.__is_right_size(arg, 30)
            f.write(arg)
        except MaxBytesError as e:
            print(e)

    def __album(self, f, fun_type, str_to_write: str = None):
        f.seek(self.tag_byte_start + 60)
        if fun_type == "r":
            return f.read(30).decode("latin-1")
        try:
            arg = str_to_write.encode("utf-8")
            self.__is_right_size(arg, 30)
            f.write(arg)
        except MaxBytesError as e:
            print(e)

    def __year(self, f, fun_type, str_to_write: str = None):
        f.seek(self.tag_byte_start + 90)
        if fun_type == "r":
            return f.read(4).decode()
        try:
            arg = str_to_write.encode("utf-8")
            self.__is_right_size(arg, 4)
            f.write(arg)
        except MaxBytesError as e:
            print(e)

    def __comment(self, f, fun_type, str_to_write: str = None):
        f.seek(self.tag_byte_start + 94)
        if fun_type == "r":
            return f.read(30).decode("latin-1")
        try:
            arg = str_to_write.encode("utf-8")
            self.__is_right_size(arg, 30)
            f.write(arg)
        except MaxBytesError as e:
            print(e)

    def __genre(self, f, fun_type, str_to_write: str = None):
        f.seek(self.tag_byte_start + 124)
        if fun_type == "r" and str_to_write == None:
            return ord(f.read(1))
        try:
            arg = bytes([int(str_to_write)])
            print(arg, type(arg))
            print(len(arg))
            self.__is_right_size(arg, 1)
            f.write(arg)
        except MaxBytesError as e:
            print(e)

    def __is_right_size(self, byte_arr: bytes, max_bytes: int):
        if len(byte_arr) > max_bytes:
            raise MaxBytesError("Text ist zu lang!")

    def str_to_bytes(self):
        ...


if __name__ == "__main__":
    rder = Mp3Reader()
    while True:
        os.system("cls")
        print("Bearbeiten:")
        print(
            "[1] Titel\n[2] Interpret\n[3] Album\n[4] Jahr\n[5] Kommentar\n[6] Genre\n"
        )
        inp = input("> ")
        try:
            fun, it = inp.split(" ")
            if fun == "read" or fun == "r":
                r = rder.read(it)
            if fun == "write" or fun == "w":
                args = input("Eingabe > ")
                rder.write(it, args)
        except (TypeError, ValueError):
            print("Eingabe nur in Zahlen 1-6. z.B 'read 1', 'write 5'")
        input()
