from dataclasses import asdict, dataclass, field
import datetime
from os import name
import urllib
import pymongo
import json
from icecream import ic

class Utils:

    @staticmethod
    def schluessel():
        with open("keys.json") as json_file:
            keys = json.load(json_file)
        return keys

    @staticmethod
    def validierung(obj: object, typen: list):
        keys, values = zip(*asdict(obj).items())
        for key, value, typ in zip(keys, values, typen):
            if type(value) != list:
                assert value, ic(f"Eingabe *{key}* kann nicht leer sein!")
                assert type(value) == typ, ic(f"{value} muss {typ} sein!")

class Datenbank:

    DB = None

    @staticmethod
    def initialisieren():
        keys = Utils.schluessel()
        client = pymongo.MongoClient("mongodb+srv://{}:{}@sfcluster.cukvo.mongodb.net/studio?retryWrites=true&w=majority".format(
            urllib.parse.quote(keys["username"]),
            urllib.parse.quote(keys["password"])
            ))

        Datenbank.DB = client["studio"]

    @staticmethod
    def kollektion_erstellen(kollektion: str, validierung_schema: dict):
        Datenbank.DB.create_collection(kollektion, validator=validierung_schema)
        #Datenbank.DB.command({"collMod": kollektion, "validator" : validierung_schema})

    @staticmethod
    def kollektion_loschen(kollektion: str):
        Datenbank.DB[kollektion].drop()

    @staticmethod
    def eins_eintragen(kollektion: str, daten: object):
        Datenbank.DB[kollektion].insert_one(asdict(daten))

    @staticmethod
    def suchen(kollektion: str, anfrage: str):
        return Datenbank.DB[kollektion].find(anfrage)

    @staticmethod
    def eins_suchen(kollektion: str, anfrage: str):
        return Datenbank.DB[kollektion].find_one(anfrage)

    @staticmethod
    def bearbeiten(kollektion: str, id: object, daten: dict):
        Datenbank.DB[kollektion].update_one(id, {"$set": daten})

    @staticmethod
    def loschen(kollektion: str, id: object):
        Datenbank.DB[kollektion].delete_one(id)


@dataclass
class Kurs():
    name: str
    teilnehmer: list[str] = field(default_factory=list, compare=False)
    datum: datetime = field(default=datetime.datetime.today(), compare=False)

    def __post_init__(self):
         Utils.validierung(self, (str, str, datetime.date, list, datetime.datetime))

@dataclass
class Teilnehmer():
    name: str
    vorname: str
    geburtsdatum: datetime.date
    kurse: list[str] = field(default_factory=list, compare=False)
    datum: datetime = field(default=datetime.datetime.today(), compare=False)

    def __post_init__(self):
        self.geburtsdatum = datetime.datetime(*self.geburtsdatum)
        Utils.validierung(self, (str, str, datetime.datetime, list, datetime.datetime))
        