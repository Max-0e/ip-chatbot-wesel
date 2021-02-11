from pymongo import MongoClient
# mit MongoDB aus standard Port laufend verbinden
client = MongoClient('mongodb://localhost:27017/')
# mit DB 'rasaBot' verbinden
db = client.rasaBot
# mit collection 'dienstleistungen' verbinden
dienstleistungen = db.dienstleistungen

synonym = "begleitete fahren ab 17"

query = { "Leistungsbeschreibung": { "$regex": synonym, "$options": 'i'} }

for dienstleistung in dienstleistungen.find(query):
    print(dienstleistung["Leistungsname"])