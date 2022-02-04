import random

stapel = []
spiel_status = "laufend"
dealer_hand = []
dealer_status = spieler_status = "spielend"  # "spielend" oder "haltend"

spieler_kontostand = 100
spieler_hand = []
spieler_einsatz = 0
spieler_status = "spielend"  # "spielend" oder "haltend"


# Gibt ein Dictionary mit den Attributen der Spielkarte, die übergeben wurden, zurück
# Jede Karte ist ein Dictionary mit 3 Einträgen, dass die Eigenschaften der Karte enthält
# @ param farbe - Die Farbe der Karte
# @ param wert - Der Wert der Karte 2, 3, 4...B, D, K, A
# @ param verdeckt - Gibt an ob die Karte verdeckt angezeigt werden soll. * * /
def lege_karte_an(wert, farbe, verdeckt=True):
    karte = {}
    karte["wert"] = wert
   #TODO ergänzen Sie die Zuweisung für die keys farbe und verdeckt im Dictionary#

    return karte


# Gibt einen String zurück, der die Karte mit Wert und Farbe repräsentiert # Beispiel: "Pik As"
def toString(karte):
    if (karte["verdeckt"]):
        return "???? ?"
    else:
        return karte["farbe"] + " " + karte["wert"]


# verdeckte Karten der übergebenen Hand werden angezeigt
def kartenAufdecken(hand):
    pass
    #TODO



# Karte vom Stapel ziehen und der übergebenen Hand geben.
# Die Karte kann dabei verdeckt oder offen auf die Hand des Spielers gegeben
# werden.
# @ param hand - Die Hand des Spielers dem die  Karte vom Stapel gegeben werden soll
# @ param verdeckt - true wenn  die Karte verdeckt übergeben werden soll

def karteGeben(hand, verdeckt):
    pass
    # TODO#


# Löscht und füllt den Kartenstapel mit 52 Karten
def stapelErstellen():
    global stapel
    farben = ["Pik", "Blatt", "Herz", "Karo"]
    werte = ["A", "K", "D", "B", "10", "9", "8", "7", "6", "5", "4", "3", "2"]

    # TODO#
    print("Stapel erstellt")


# Mischt den Kartenstapel durch.
# Jede Karte wird mit einer
# Karte an einer zufälligen Stelle getauscht

# Teilt die jeweils 2 Karten für die erste Runde aus
def kartenFürErsteRundeGeben():
    # Teilnehmer auf status "spielend" setzen und Blatt auf der Hand löschen
    global spieler_status, dealer_status, status, spiel_status, dealer_hand, spieler_hand

    spieler_status = "spielend"
    dealer_status = "spielend"
    spiel_status = "laufend"
    dealer_hand.clear()
    spieler_hand.clear()

    # 2 Karten pro Spieler ausgeben
    karteGeben(dealer_hand, False)
    karteGeben(spieler_hand, False)
    karteGeben(dealer_hand, True)
    karteGeben(spieler_hand, False)

    # Zeigt die Karten der Spieler und den aktuellen Einsatz sowie Kontostand  des Spielers


# Zählt die Punkte auf der hand des Spielers.Asse werden bestmöglich mit 1 oder 11 gezählt
def punkteAufDerHand(hand):
    punkte = 0
    asse = 0    # Anzahl der Asse die mit einem Punkt gezählt werden.

    # Zähle die Kartenwerte (punkte) und die Asse. Asse zählen zunächst als 1, werden später gesondert betrachtet

        # TODO#


    # Ersetze die 1-Punkt-Asse wenn möglich durch 11-Punkt-Asse
    while punkte + 10 <= 21 and asse > 0:
        asse -= 1
        punkte += 10

    return punkte


def spielzustandAnzeigen():
    print("===============================")
    print("Black Jack")
    print("===============================")
    print("Karten des Dealers:")
    zustand = ""

    print(zustand)

    print("Karten des Spielers:")
    zustand = ""

    print(zustand)
    print("")
    print("Punkte auf der Hand:", punkteAufDerHand(spieler_hand))


def einsatzGeben():
    global spieler_kontostand
    global spieler_einsatz
    print("Dein Konstostand beträgt:", spieler_kontostand)
    spieler_einsatz = int(input("Mit welchem Einsatz möchtest Du spielen?"))
    spieler_kontostand -= spieler_einsatz


# fragt den Spieler auf der Konsole, ob er weiter spielen möchte und setzt
# dessen Status entsprechend
def haltenOderZiehen():
    global spieler_status
    readLine = input("Möchtest Du eine weitere Karte ziehen (j/n)?")
    if readLine.lower() == ("n"):
        spieler_status = "haltend"


def gewinnerErmittelnUndAuszahlen():
    global spieler_einsatz
    global spieler_kontostand
    kartenAufdecken(dealer_hand)

    spielzustandAnzeigen()
    print("Punkte des Dealers:", punkteAufDerHand(dealer_hand))

    # Unentschieden
    if punkteAufDerHand(spieler_hand) == punkteAufDerHand(dealer_hand):
        spieler_kontostand += spieler_einsatz
        print("Unentschieden!")

    # Spieler gewinnt mit Black Jack
    elif False: #TODO Bedingung ergänzen#
        spieler_kontostand += spieler_einsatz * 2.5
        print("Bravo! Ein echter Black Jack. Sieg auf ganzer Linie! Sie erhalten das 2,5 fache des Einsatzes")

    # Spieler gewinnt ohne Black Jack
    elif False:#TODO Bedingung ergänzen #
        spieler_kontostand += spieler_einsatz * 2
        print("\nSieg! Sehr gut, Sie haben ihren Einsatz verdoppelt.")

    # Dealer gewinnt
    else:
        print("Ups, verloren! Versuch's doch noch mal!")

    spieler_einsatz = 0


# Gibt jedem Spieler die Möglichkeit eine Karte ziehen oder zu halten
def rundeSpielen():
    global dealer_status
    global spieler_status
    global spiel_status
    # Zug        des        Spielers
    if (spieler_status == "spielend"):

        if (punkteAufDerHand(spieler_hand) >= 21):
            spieler_status = "haltend"
        else:
            haltenOderZiehen()

        # Der Status  des Spielers kann sich durch HaltenOderZiehen() geändert haben,
        # daher wird erneut geprüft.
        if spieler_status == "spielend":
            karteGeben(spieler_hand, False)
        else:
            spieler_status = "haltend"

        # Zug des Dealers

    if punkteAufDerHand(dealer_hand) <= 14:
        karteGeben(dealer_hand, True)
    else:
        dealer_status = "haltend"
    if spieler_status == "haltend" and dealer_status == "haltend":
        spiel_status = "beendet"


# Startet eine Runde des Spiels. Die Kontostand wird beibehalten.
def spielStarten():

    einsatzGeben()
    kartenFürErsteRundeGeben()

    # Schleife für Spielrunden
    # Lässt spieler und dealer eine Runde spielen(max eine
    # Karte pro Spieler)
    while spiel_status == "laufend":
        spielzustandAnzeigen()
        rundeSpielen()
    gewinnerErmittelnUndAuszahlen()


def main():
    stapelErstellen()
    eingabe = "j"
    while (eingabe == "j"):
        spielStarten()
        eingabe = input("\nMöchtest Du weiterspielen (j/n)?").lower() 

main()