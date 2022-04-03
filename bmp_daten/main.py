class BMPMetaData:
    def __init__(self, dateiname: str) -> None:
        self.__dateiname: str = dateiname
        self.__hoehe: int = None
        self.__breite: int = None
        self.is_valid()

    def is_valid(self):
        with open(self.__dateiname, "rb") as f:
            if f.read(2) != b'BM':
                assert Exception("Keine BMP Datei!")

    def __str__(self) -> str:
        with open(self.__dateiname, "rb") as f:
            f.seek(18)
            h = int.from_bytes(f.read(4), byteorder="little",signed=True)
            b = int.from_bytes(f.read(4), byteorder="little",signed=True)
        return f"Datei: {self.__dateiname}, Höhe: {h}, Breite: {b}"

    def schreibe_text_datei(self, dateipfad: str, anhaengen: bool=False) -> None:
        if anhaengen: anh="a"
        else: anh="w"
        with open(dateipfad, anh) as f:
            f.write(self.__str__() + "\n")

if __name__ == "__main__":
    # pf = input("pfad > ")
    # ho = input("hoehe > ")
    # br = input("breite > ")
    bmp = BMPMetaData("test1.bmp")
    print(bmp)
    bmp.schreibe_text_datei("class.txt")
    