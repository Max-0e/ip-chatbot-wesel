const mongoose = require('mongoose');
const fs = require('fs');

// create Schema & Models for 'Dienstleistung'
const dienstleistungSchema = new mongoose.Schema({
    LeistungsID: { type: String, required: true },
    Leistungsname: { type: String, required: true },
    LeistungsURI: { type: String, required: true },
    Leistungsbeschreibung: { type: String, required: true },
    Fachinformationen: { type: Object, required: true },
    Ansprechpunkt: { type: Array, required: true },
    Aktualisierungszeitpunkt: { type: Date, required: true },
    BotAntwort: { type: Array, required: false }
});
dienstleistungSchema.set('collection', 'dienstleistungen');
const Dienstleistung = mongoose.model('Dienstleistung', dienstleistungSchema);

// set up variables for local MongoDB installation
const DB_URL = 'mongodb://localhost/';
const DB_DB = 'rasaBot';

// establish Database Connection to local mongoDB
function connectDB () {
    mongoose.connect(`${DB_URL}${DB_DB}`, { useNewUrlParser: true, useUnifiedTopology: true, useFindAndModify: false });
    const db = mongoose.connection;
    db.on('error', console.error.bind(console, 'connection error:'));
    db.once('open', () => {
        console.log(`Database connection established`);
        console.log('Copy Output to Database...')
        // Dienstleistung.create
        readOutputJSONAndFillDB();
    });
} 

async function readOutputJSONAndFillDB () {
    // Daten aus output.json lesen
    const rawData = fs.readFileSync('output.json');
    const data = JSON.parse(rawData);
    // Datum und Uhrzeit als Timestamp speichern
    const aktualisierungszeitpunkt = new Date();
    // DB mit den Daten aus output.json füllen
    for (let [bez, dienstleistung] of Object.entries(data)){
        // erstellen eines neuen Dienstleistungsobjekts
        const exists = await Dienstleistung.findOneAndUpdate({ LeistungsID: dienstleistung.LeistungsID}, dienstleistung);
        if (exists) {
            console.log(dienstleistung.Leistungsname + ' wurde aktualisiert.')
        } else {
            let newDienstleistung = new Dienstleistung ({
                _id: new mongoose.Types.ObjectId(),
                LeistungsID: dienstleistung.LeistungsID,
                Leistungsname: dienstleistung.Leistungsname,
                LeistungsURI: dienstleistung.LeistungsURI,
                Leistungsbeschreibung: dienstleistung.Leistungsbeschreibung,
                Fachinformationen: dienstleistung.Fachinformationen,
                Ansprechpunkt: dienstleistung.Ansprechpunkt,
                Aktualisierungszeitpunkt: aktualisierungszeitpunkt,
                BotAntwort: []
            });
            // speichern der neuen Dienstleistung
            try {
                await newDienstleistung.save();
                console.log(dienstleistung.Leistungsname + ' wurde gespeichert.')
            } catch (e) {
                console.log(e);
            }
        }
        
    }
    console.log('done... disconnecting now')
    mongoose.disconnect();
}

connectDB();