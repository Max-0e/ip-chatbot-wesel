from pymongo import MongoClient
# mit MongoDB aus standard Port laufend verbinden
client = MongoClient('mongodb://ip-chatbot-wesel.dnsuser.de:27017/')
# mit DB 'rasaBot' verbinden
db = client.rasaBot
# mit collection 'dienstleistungen' verbinden
dienstleistungen = db.dienstleistungen

intent = "Artenschutz – Meldepflicht"

query = { "Leistungsname": { "$regex": intent, "$options": 'i'} }

for dienstleistung in dienstleistungen.find(query):
    print(dienstleistung["Leistungsname"])