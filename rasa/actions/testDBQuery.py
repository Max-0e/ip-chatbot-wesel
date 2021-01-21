from pymongo import MongoClient

# mit MongoDB aus standard Port laufend verbinden
client = MongoClient('mongodb://localhost:27017/')
# mit DB 'rasaBot' verbinden
db = client.rasaBot
# mit collection 'dienstleistungen' verbinden
dienstleistungen = db.dienstleistungen

dbGefunden = dienstleistungen.find()

if dbGefunden:
    print("***************************************\n*** Datenbankverbindung erfolgreich *** \n***************************************")
else:
    print("***************************************\n***** Ein Fehler ist aufgetreten ****** \n***************************************")