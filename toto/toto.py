import random

TabelleT = dict[int, int]

anzahl_spieler: int = 1  # int(input())
runden: int = 6  # int(input())

ergebnisse: dict[str, int] = {}

def zeige_ergebnisse(ergebnisse: dict[str, int] = ergebnisse):
    print("Spieler\tErgebnis")
    for spieler, ergebnis in ergebnisse.items():
        print(f"{spieler}\t{ergebnis}")

def generiere_tabelle(runden: int) -> dict:
    toto_tabelle: dict = {}

    for runde in range(1, runden+1):
        toto_tabelle.update({runde: 0})

    return toto_tabelle


def zeige_tabelle(tabelle: TabelleT) -> None:
    print("Multiplikator\tZahl\tErgebnis")

    for multiplikator, zahl in tabelle.items():
        print(f"{multiplikator}x\t\t{zahl}\t{multiplikator*zahl}")
    print(f"\n\t\tGesamt: {rechne_ergebnis(tabelle)}")


def rechne_ergebnis(tabelle: TabelleT) -> int:
    ergebnis = 0

    for multiplikator, zahl in tabelle.items():
        ergebnis += multiplikator * zahl

    return ergebnis


def zahl_einfugen(tabelle: TabelleT, multiplikator: int, zahl: int) -> dict:
    if 6 < zahl < 1:
        tabelle[multiplikator] = zahl
    else:
        raise ValueError
    return tabelle

def main() -> None:
    for _ in range(anzahl_spieler):
        spieler_name: str = "ok"#input("[>] Dein Name: ")
        toto_tabelle: list = generiere_tabelle(runden)

        for runde in range(runden):
            print(f"Versuch: {runde}")
            zufallszahl = random.randint(1, 6)
            zeige_tabelle(toto_tabelle)
            print(f"\n[!] Zufallszahl: {zufallszahl}\n")
            multiplikator = int(input("[>] Platz?: "))
            try:
                toto_tabelle = zahl_einfugen(toto_tabelle, multiplikator, zufallszahl)
            except ValueError:
                runde -= 1
                print("[x] Multiplikator nur zwischen 1 und 6!")
            print("")

        ergebnisse.update({spieler_name: rechne_ergebnis(toto_tabelle)})

    zeige_ergebnisse()

if __name__ == '__main__':
    main()