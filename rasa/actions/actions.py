# Custome Action für allgemeines Querien der MongoDB
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from pymongo import MongoClient

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
        # letzte Intent aus dem Tracker-Objekt holen
        dienstleistung_slot = tracker.slots["dienstleistung"]
        print(dienstleistung_slot)

        # Query mit letztem Intent: dieser entspricht dem Infonamen in der Datenbank
        query = { 
            "Leistungsname": { "$regex": dienstleistung_slot},
        }
        # config-Datenbank mit Query durchsuchen
        dienstleistung = dienstleistungen.find_one(query)
        print(dienstleistung)
        # info und dazugehöriges Template zum Bot zurücksenden
        dispatcher.utter_message(text=f'{dienstleistung["LeistungsURI"]}')

        return []