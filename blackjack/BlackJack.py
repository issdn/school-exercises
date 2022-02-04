import random


class Dealer:
    def __init__(self) -> None:
        self.hand: list = []


class Spieler(Dealer):
    def __init__(self, name: str) -> None:
        super().__init__(self)
        self.name: str = name
        self.konto_stand: int = 100

    def zeig_konto_stand(self) -> None:
        print(f"Kontostand des Spielers {self.name} betragt {self.konto_stand}.")

    def einsatz_geben(self) -> int:
        try:
            einsazt = int(input("Mit welchem Einsatz möchtest Du spielen?"))
        except ValueError:
            print("Einsatz muss eine Zahl sein!")
        if self.konto_stand - einsazt < 0:
            print("Dein Kontostand ist zu klein!")
            self.zeig_konto_stand()
            self.einsatz_geben()
        self.konto_stand -= einsazt
        return einsazt

    def naechste_runde(self) -> bool:
        w_s = input("Willst Du weiter spielen?").lower()
        if w_s == "j" or w_s == "ja":
            return True
        elif w_s == "n" or w_s == "nein":
            return False
        else:
            print("ja/nein ; j/n")
            self.naechste_runde()


class Tisch:
    def __init__(self) -> None:
        self.stapel: list = []
        self.naechste_runde = True
        self.spieler = Spieler(name="Karol")
        self.dealer = Dealer()
        self.spiel_starten()

    def stapel_erstellen(self) -> dict:
        farben = ["Pik", "Blatt", "Herz", "Karo"]
        werte = ["A", "K", "D", "B", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        geordn_stapel = [
            {"farbe": farbe, "wert": wert} for farbe in farben for wert in werte
        ]
        self.stapel = random.shuffle(geordn_stapel)

    def spiel_starten(self) -> None:
        self.stapel_erstellen()
        spieler_name = input("Dein Name: ")
        self.stapel_erstellen()
        self.karten_fur_erste_runde_geben()
        # self.spiel_schleife(naechste_runde=spieler.naechste_runde)

    def karten_fur_erste_runde_geben(self) -> None:
        self.karte_geben(spieler, verdeckt=False)

    def karte_geben(spieler, verdeckt) -> None:
        spieler.hand.append()

    def toString(karte):
        if karte["verdeckt"]:
            return "[ ? ]"
        else:
            return f"[ {karte['farbe']} {karte['wert']} ]"

    def spiel_schleife(naechste_runde):
        ...


tisch = Tisch()
