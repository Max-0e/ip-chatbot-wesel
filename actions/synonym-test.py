from pymongo import MongoClient
# mit MongoDB aus standard Port laufend verbinden
client = MongoClient('mongodb://0.0.0.0:27017/')
# mit DB 'rasaBot' verbinden
db = client.rasaBot
# mit collection 'dienstleistungen' verbinden
dienstleistungen = db.dienstleistungen

synonym = "Verlust eines Fahrzeugbriefes"

query = { "Leistungsbeschreibung": { "$regex": synonym, "$options": 'i'} }

for dienstleistung in dienstleistungen.find(query):
    print(dienstleistung["Leistungsname"])