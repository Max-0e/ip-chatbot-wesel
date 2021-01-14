# Custome Action für allgemeines Querien der MongoDB
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from pymongo import MongoClient


class ActionSearchDB(Action):

    def name(self) -> Text:
        return "action_search_db"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # mit MongoDB auf standard Port laufend verbinden
        client = MongoClient('mongodb://localhost:27017/')
        # mit DB 'rasaBot' verbinden
        db = client.rasaBot
        # mit collection 'dienstleistungen' verbinden
        dienstleistungen = db.dienstleistungen
        # erstellen eines queries mit der Suche nach de letzten Intent
        query = { 
            "Leistungsname": { "$regex": "Begleitest"},
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
