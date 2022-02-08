import random
import os
from turtle import pu


def clear():
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


class Karte:
    def __init__(self, wert: str, farbe: str) -> None:
        self.wert: str = wert
        self.farbe: str = farbe
        self.verdeckt: bool = False
        self.punkte: int = 0
        self._punkte()

    def _punkte(self):
        besondere_werte = ["A", "K", "D", "B"]
        if self.wert in besondere_werte:
            if self.wert == "A":
                self.punkte = 1
            else:
                self.punkte = 10
        else:
            self.punkte += int(self.wert)

    def wechseln(self):
        if self.wert == "A":
            if self.punkte == 1:
                self.punkte = 11
            else:
                self.punkte = 1

    def __str__(self):
        if self.verdeckt:
            return "[ ? ]"
        else:
            return f"[ {self.farbe} {self.wert} ]"


class Dealer:
    def __init__(self) -> None:
        self.hand: list = []

    def hand_zeigen(self) -> None:
        print(f"{self.__class__.__name__} Hand: ", end="")
        for karte in self.hand[:-1]:
            print(karte, end="")
        print(self.hand[-1])

    def punkte_auf_der_hand(self) -> int:
        punkte: int = 0

        for karte in self.hand:
            punkte += karte.punkte

        return punkte

    def karten_aufdecken(self) -> None:
        print(f"{self.__class__.__name__} Hand: ", end="")
        for karte in self.hand:
            karte.verdeckt = False
        for karte in self.hand[:-1]:
            print(karte, end="")
        print(self.hand[-1])

    def asse_listen(self) -> list:
        asse = []
        for karte in self.hand:
            if karte.wert == "A":
                asse.append(karte)
        return asse


class Spieler(Dealer):
    def __init__(self) -> None:
        super().__init__()
        self.konto_stand: int = 100
        self.einsatz: int = 0

    def zeig_konto_stand(self) -> None:
        print(f"Dein Kontostand betragt: {self.konto_stand}.")

    def einsatz_geben(self) -> int:
        try:
            einsazt = int(input("[?] Mit welchem Einsatz möchtest Du spielen?: "))
            if (self.konto_stand - einsazt) < 0:
                print("Dein Kontostand ist zu klein!")
                self.zeig_konto_stand()
                self.einsatz_geben()
            else:
                self.konto_stand -= einsazt
                self.einsatz = einsazt
        except ValueError:
            print("Einsatz muss eine Zahl sein!")
            self.einsatz_geben()

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
        self.spieler = Spieler()
        self.dealer = Dealer()
        self.spiel_starten()

    def stapel_erstellen(self, decks: int = 2) -> dict:
        farben = ["Pik", "Blatt", "Herz", "Karo"]
        werte = ["A", "K", "D", "B", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        self.stapel = [Karte(wert, farbe) for farbe in farben for wert in werte]
        random.shuffle(self.stapel)

    def spiel_starten(self) -> None:
        clear()
        self.spieler.hand.clear()
        self.dealer.hand.clear()
        self.stapel_erstellen()
        self.karten_fur_erste_runde_geben()
        print("*----BLACKJACK----*\n")
        if self.spieler.konto_stand == 0:
            print("Du hast kein Geld mehr!")
            exit()
        print("Dein Kontostand: %d\n" % self.spieler.konto_stand)
        self.spieler.hand_zeigen()
        self.dealer.hand_zeigen()
        print()
        self.spieler.einsatz_geben()
        self.spiel_verlauf()
        self.gewinner_ermitteln_und_auszahlen()

    def spiel_verlauf(self) -> None:
        errors = []
        fertig = False
        while not fertig:
            clear()
            print("*----BLACKJACK----*")
            print()
            for error in errors:
                print(error)
            errors.clear()
            print("Dein Kontostand: ", self.spieler.konto_stand)
            print("Dein Einsatz: %d\n" % self.spieler.einsatz)
            self.spieler.hand_zeigen()
            print("Deine Punkte: %d" % self.spieler.punkte_auf_der_hand())
            self.dealer.hand_zeigen()
            print("\n[1] Ziehen.")
            print("[2] Karten aufdecken.")
            print("[X] Spiel verlassen.")
            asse = self.spieler.asse_listen()
            if asse:
                print("[3] Punkte fur Ass wechseln.")

            wahl = input("\n[?] ")

            if wahl == "1":
                self.karte_geben(self.spieler, False)
            elif wahl == "2":
                break
            elif wahl == "3" and asse != 0:
                self.asse_behandeln(asse)
            elif wahl.lower() == "x":
                exit()
            else:
                errors.append("Eingabe nur in Zahlen aus der Liste!")
                continue

    def gewinner_ermitteln_und_auszahlen(self):
        self._dealer_ai()
        print()
        spieler_p = self.spieler.punkte_auf_der_hand()
        dealer_p = self.dealer.punkte_auf_der_hand()
        self.spieler.karten_aufdecken()
        print("Spieler Punkte: %d" % spieler_p)
        self.dealer.karten_aufdecken()
        print("Dealer Punkte: %d" % dealer_p)
        print()
        potenzielles_gewinn = self.spieler.einsatz * 2
        if spieler_p > dealer_p:
            if spieler_p <= 21:
                print("GEWONNEN! + %d" % potenzielles_gewinn)
                self.spieler.konto_stand += potenzielles_gewinn
            elif spieler_p > 21 and dealer_p > 21:
                print("Stillstand. + %d" % self.spieler.einsatz)
                self.spieler.konto_stand += potenzielles_gewinn / 2
            elif spieler_p > 21 and dealer_p <= 21:
                print("Verloren! - %d" % self.spieler.einsatz)
        elif dealer_p > spieler_p:
            if dealer_p <= 21:
                print("Verloren! - %d" % self.spieler.einsatz)
            elif spieler_p > 21 and dealer_p > 21:
                print("Stillstand. + %d" % self.spieler.einsatz)
                self.spieler.konto_stand += potenzielles_gewinn / 2
            elif dealer_p > 21 and spieler_p <= 21:
                print("GEWONNEN! + %d" % potenzielles_gewinn)
                self.spieler.konto_stand += potenzielles_gewinn
        ende = input("\n[ENTER]")
        self.spiel_starten()

    def asse_behandeln(self, asse: list, error=False, error_msg=""):
        fertig = False
        while not fertig:
            clear()
            if error:
                print(error_msg)
            print("Punkte gesamt: %d" % self.spieler.punkte_auf_der_hand())

            for i, a in enumerate(asse):
                print(f"Punkte fur Ass ({i+1}): {a.punkte}")
            print("\n[A] Um zu wechseln, gib Zahl eines Asses aus der Liste ein.")
            print("[9] Verlassen.")
            x = input("\n[?] ")
            try:
                if x == "1":
                    asse[0].wechseln()
                elif x == "2" and asse[1]:
                    asse[1].wechseln()
                elif x == "3" and asse[2]:
                    asse[2].wechseln()
                elif x == "4" and asse[3]:
                    asse[3].wechseln()
                elif x == "9":
                    fertig = True
                else:
                    self.asse_behandeln(
                        asse, True, "Eingabe nur in Zahlen aus der Liste!"
                    )
            except IndexError:
                self.asse_behandeln(asse, True, f"Du hast nur {len(asse)} Asse!\n")

    def karten_fur_erste_runde_geben(self) -> None:
        self.karte_geben(self.spieler, verdeckt=False)
        self.karte_geben(self.dealer, verdeckt=True)
        self.karte_geben(self.spieler, verdeckt=False)
        self.karte_geben(self.dealer, verdeckt=True)

    def test_karte_geben(self, spieler):
        karte = Karte(wert="A", farbe="Karo")
        spieler.hand.append(karte)

    def karte_geben(self, spieler, verdeckt) -> None:
        karte = self.stapel.pop(0)
        karte.verdeckt = verdeckt
        spieler.hand.append(karte)

    def karte_zeigen(self, karte) -> None:
        if karte.verdeckt:
            print("[ ? ]")
        else:
            print(f"[ {karte.farbe} {karte.wert} ]")

    def _dealer_ai(self):
        fertig = False
        asse = self.dealer.asse_listen()
        while not fertig:
            punkte = self.dealer.punkte_auf_der_hand()
            if punkte > 13:
                # print("Punkte uber 13. Fertig. Punkte: %d" % punkte)
                fertig = True
            elif asse and punkte <= 10:
                for ass in asse:
                    if punkte <= 10 and ass.punkte == 1:
                        ass.wechseln()
                        # print(
                        #     "Punkte unter 10, ass wechseln. Punkte %d"
                        #     % self.dealer.punkte_auf_der_hand()
                        # )
                        punkte = self.dealer.punkte_auf_der_hand()
                    elif punkte > 21 and ass.punkte == 11:
                        ass.wechseln()
                        # print(
                        #     "Punkte uber 21. Ass wechseln. Punkte: %d"
                        #     % self.dealer.punkte_auf_der_hand()
                        # )
                        punkte = self.dealer.punkte_auf_der_hand()
            elif punkte <= 13:
                self.karte_geben(self.dealer, True)
                # print(
                #     "Punkte unter 14, Karte ziehen. Punkte: %d"
                #     % self.dealer.punkte_auf_der_hand()
                # )


def main() -> None:
    Tisch()


if __name__ == "__main__":
    main()
