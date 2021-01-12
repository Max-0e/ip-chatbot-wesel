from pymongo import MongoClient

# mit MongoDB aus standard Port laufend verbinden
client = MongoClient('mongodb://localhost:27017/')
# mit DB 'rasaBot' verbinden
db = client.rasaBot
# mit collection 'dienstleistungen' verbinden
dienstleistungen = db.dienstleistungen

query = { 
    "Leistungsname": { "$regex": "Be"},
    "Leistungsbeschreibung": { "$regex": "Fahrerlaubnis"} 
 }
counter = dienstleistungen.count_documents(query)
    
if counter == 1 :
    print(dienstleistungen.find_one(query))
elif counter == 0:
    print('kein ergebnis')
else:
    print(counter)