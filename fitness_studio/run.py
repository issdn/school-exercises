from FStudio import Datenbank, Kurs, Teilnehmer, Utils
import datetime

kursValidation = {
    "$jsonSchema":{
    
    "bsonType": "object",
    "required": ["name", "datum"],
    "properties": {
        "name": {
            "bsonType": "string",
            "description": "Muss string sein!"
            },
        "teilnehmer": {
            "bsonType": "array"
            }
        }
    }
}

teilnehmerValidation = {
    "$jsonSchema":{
    
    "bsonType": "object",
    "required": ["vorname", "name", "geburtsdatum"],
    "properties": {
        "name": {
            "bsonType": "string",
            "description": "Inkorrekte name!"
            },
        "vorname": {
            "bsonType": "string",
            "description": "Inkorrekte vorname!"
            },
        "geburtsdatum": {
            "bsonType": "date"
            },
        "kurse": {
            "bsonType": "array"
            },
        "datum": {
            "bsonType": "date"
            }
        }
    }
}

def main():
    Datenbank.initialisieren()
    Datenbank.kollektion_loschen("Teilnehmer")
    Datenbank.kollektion_erstellen("Teilnehmer", teilnehmerValidation)
    t1 = Teilnehmer("ok", "kaka", (2000,12,12))
    Datenbank.eins_eintragen("Teilnehmer", t1)

if __name__ == "__main__":
    main()