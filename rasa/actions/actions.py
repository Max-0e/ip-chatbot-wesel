# Custome Action für allgemeines Querien der MongoDB
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from pymongo import MongoClient

import random
import re

# mit MongoDB auf standard Port laufend verbinden
client = MongoClient('mongodb://localhost:27017/')
# mit DB 'rasaBot' verbinden
db = client.rasaBot
# mit collection 'dienstleistungen' verbinden
dienstleistungen = db.dienstleistungen
#mit collection 'config' verbinden
config = db.config
class ActionSearchDB(Action):

    def name(self) -> Text:
        return "action_search_db"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # erstellen eines queries mit der Suche nach de letzten Intent
        query = { 
            "Leistungsname": { "$regex": "Begleitet"},
            # "Leistungsbeschreibung": { "$regex": tracker.latestet_message.intent} 
        }
        # erstes durchsuchen der Datenbank nach dem Suchbegriff
        counter = dienstleistungen.count_documents(query)
        # je nachdem wie viele ergebisse gefunden wurden werden entsprechende Antworten gegeben
        if counter == 1 :
            dienstleistung = dienstleistungen.find_one(query)
            print(dienstleistung["Leistungsname"])
            dispatcher.utter_message(text=f'Schau doch mal hier:{dienstleistung["LeistungsURI"]}')
        elif counter == 0:
            print('kein ergebnis')
            dispatcher.utter_message(text="Dazu kann ich dir leider nicht weiter helfen.")
        else:
            print(counter)
            dispatcher.utter_message(text=f'Ich bin mir noch nicht sicher was du genau meinst. Es kommen aktuell {counter} Einträge für dich in Frage.')

        return []

class ActionSearchConfigDB(Action):

    def name(self) -> Text:
        return "action_search_configdb"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # letzte Intent aus dem Tracker-Objekt holen
        last_intent = tracker.latest_message["intent"]["name"]

        # Query mit letztem Intent: dieser entspricht dem Infonamen in der Datenbank
        query = { 
            "infoname": { "$regex": last_intent},
        }
        # config-Datenbank mit Query durchsuchen
        dienstleistung = config.find_one(query)
        # info und dazugehöriges Template zum Bot zurücksenden
        dispatcher.utter_message(template=f'utter_static_{last_intent}', info=f'{dienstleistung["infoinhalt"]}')

        return []

class dispatcher_test(Action):

    def name(self) -> Text:
        return "action_dispatcher_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template = "utter_dbresponse_öz",
                                 kategorie = "EingabeKategorie",
                                 öffnungszeiten = "18:00 Uhr - 20:00 Uhr")

        dispatcher.utter_message(template = "utter_dbresponse_ansprechpartner",
                                 kategorie = "EingabeKategorie",
                                 anschrift = "Adresse hier")

        dispatcher.utter_message(template = "utter_dbresponse_allgemein",
                                 kategorie = "EingabeKategorie",
                                 link = "https://www.kreis-wesel.de")

        dispatcher.utter_message(template = "utter_dbresponse_zwei_ergebnisse",
                                 kategorie1 = "Diesekategorie",
                                 kategorie2 = "AndereKategorie")

        dispatcher.utter_message(template = "utter_dbresponse_zu_viele_ergebnisse")

        dispatcher.utter_message(template = "utter_dbresponse_kein_ergebnis")

        return []

class ActionSearchDienstleistung(Action):

    def name(self) -> Text:
        return "action_search_dienstleistung"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Inhalt der Slots abfragen
        dienstleistung_slot = tracker.slots["dienstleistung"]
        anliegen_slot = tracker.slots["anliegen"]

        print(dienstleistung_slot)
        print(anliegen_slot)

        # Query mit letztem Intent: dieser entspricht dem Infonamen in der Datenbank
        
        query = { 
            "Leistungsname": { "$regex": dienstleistung_slot},
        }
        # config-Datenbank mit Query durchsuchen
        dienstleistung = dienstleistungen.find_one(query)
        if dienstleistungen.count_documents(query) == 0 :
            return [SlotSet("dienstleistung", None)]

        # Anliegen Öffnungszeiten
        if anliegen_slot == "öffnungszeiten" :
            oeffnungszeiten = ""
            if "Oeffnungszeiten" in dienstleistung["Ansprechpunkt"][0] :
                oeffnungszeiten = dienstleistung["Ansprechpunkt"][0]["Oeffnungszeiten"]
                print("Öffnungszeit gefunden")
            else :
                query = { 
                    "infoname": { "$regex": "öffnungszeiten"},
                }
                config_oez = config.find_one(query)
                oeffnungszeiten = config_oez["infoinhalt"]
                print("Keine Öffnungszeit gefunden, default wird genommen")
            dispatcher.utter_message(template = "utter_dbresponse_öz",
                                     kategorie = dienstleistung["Leistungsname"],
                                     öffnungszeiten = oeffnungszeiten)
        # Anliegen Telefun
        elif anliegen_slot == "telefon" :
            telefon = ""
            regex = re.compile(r'[a-zA-Z]')
            ansprechpartner = dienstleistung["Ansprechpunkt"][0]["Ansprechpartner"]
            name = ansprechpartner["NameAnsprechpartner"]["Anrede"] + " " + ansprechpartner["NameAnsprechpartner"]["Familienname"]["Name"]
            for element in ansprechpartner["AnsprechpartnerKontaktmoeglichkeit"] :
                if not regex.search(element["Kennung"]) :
                    telefon = element["Kennung"] # erste Telefonnummer wird genommen
                    print("Telefonnummer gefunden")
                    break
            
            if telefon == "" : # Wenn es keine Telefonnummer gibt, wird der Default genommen
                query = { 
                    "infoname": { "$regex": "telefon"},
                }
                config_tele = config.find_one(query)
                telefon = config_tele["infoinhalt"]
                print("Keine Telefonnummer gefunden, default wird genommen")
            dispatcher.utter_message(template = "utter_dbresponse_telefon",
                                     kategorie = dienstleistung["Leistungsname"],
                                     person = name,
                                     telefon = telefon)
        # Anliegen E-Mail
        elif anliegen_slot == "email" :
            email = ""
            regex = re.compile(r'[a-zA-Z]')
            ansprechpartner = dienstleistung["Ansprechpunkt"][0]["Ansprechpartner"]
            name = ansprechpartner["NameAnsprechpartner"]["Anrede"] + " " + ansprechpartner["NameAnsprechpartner"]["Familienname"]["Name"]
            for element in ansprechpartner["AnsprechpartnerKontaktmoeglichkeit"] :
                if regex.search(element["Kennung"]) :
                    email = element["Kennung"] # erste Mailadresse wird genommen
                    print("Email-Adresse gefunden")
                    break
            
            if email == "" : # Wenn es keine Email gibt, wird der Default genommen
                query = { 
                    "infoname": { "$regex": "email"},
                }
                config_email = config.find_one(query)
                email = config_email["infoinhalt"]
                print("Keine Email-Adresse gefunden, default wird genommen")
            dispatcher.utter_message(template = "utter_dbresponse_email",
                                     kategorie = dienstleistung["Leistungsname"],
                                     person = name,
                                     email = email)
        # Anliegen Anschrift
        elif anliegen_slot == "ansprechpartner" :
            adresse = ""
            if "AnsprechpunktAnschrift" in dienstleistung["Ansprechpunkt"] :
                regex = re.compile(r'([0-9]+.*)') # Regex für Hausnummer + Anhang bsp. 12a
                adr = dienstleistung["Ansprechpunkt"]["AnsprechpunktAnschrift"]
                hausnummer = regex.search(adr["Hausnummer"])
                adresse = adr["Strasse"] + " " + hausnummer.group(0) + " " + adr["Postleitzahl"] + " " + adr["Ort"]
                print("Adresse gefunden")
            if adresse == "" : # Wenn es keine Adresse gibt, wird der Default genommen # Reeser Landstraße 31 46383 Wesel
                query = { 
                    "infoname": { "$regex": "adresse"},
                }
                config_adresse = config.find_one(query)
                adresse = config_adresse["infoinhalt"]
                print("Keine Telefonnummer gefunden, default wird genommen")
            dispatcher.utter_message(template = "utter_dbresponse_ansprechpartner",
                                     kategorie = dienstleistung["Leistungsname"],
                                     anschrift = adresse)
        # Allgemeine Informationen
        else :
            print("Ausgabe allgemeine Informationen")
            if len(dienstleistung["BotAntwort"]) > 0 :
                dispatcher.utter_message(template = "utter_dbresponse_allgemein_antworttext",
                                         info = f'{dienstleistung["BotAntwort"][random.randrange(0, len(dienstleistung["BotAntwort"]))]} Hier sind noch weitere Informationen',
                                         kategorie = dienstleistung["Leistungsname"],
                                         link = dienstleistung["LeistungsURI"])
            else :     
                dispatcher.utter_message(template = "utter_dbresponse_allgemein",
                                         kategorie = dienstleistung["Leistungsname"],
                                         link = dienstleistung["LeistungsURI"])

        return [SlotSet("anliegen", None)]