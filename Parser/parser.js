const https    = require('follow-redirects').https;
const convert  = require('xml-js');
const fs       = require('fs');

const URL = 'https://www.kreis-wesel.de';
const OBJECT_KEYS = ['Leistungsname',
                     'LeistungsURI',
                     'Leistungsbeschreibung',
                     'Fachinformationen',
                     'Ansprechpunkt'];

createJSON();

function findObjByKey(obj, name) {
    if (obj.hasOwnProperty(name)) return obj[name];
    for (let child in obj) {
        if (typeof(obj[child]) == 'object' || typeof(obj[child]) == 'array') {
            let temp = findObjByKey(obj[child], name);
            if(temp) return temp;        
        }
    }
    return false;
}

function httpsRequest(url) {
    return new Promise((resolve, reject) =>{
        https.get(url, (res) => {
            var data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            res.on('end', () => {
                resolve(data);
            });
            res.on('error', (error) => {
                reject(error);
            })
        });
    })
}

async function createJSON() {
    var overview = await httpsRequest(URL + '/d115');

    var regEx = /<a.*?href="(?<path>.*?)".*?>(?<name>.*?)<\/a>/gm; //Matcht Link und Name der einzelnen XML Files
    var found = overview.matchAll(regEx);
    var output = {};
    for(let element of found) {
        if(element.groups.name.includes('Führerschein')) {
            let outputObj = {};
            let xml = await httpsRequest(URL + element.groups.path);
            let tempObj = convert.xml2js(xml, { compact: true, ignoreDeclaration: true, ignoreAttributes: true });
            OBJECT_KEYS.forEach(key => {
                let foundObj = findObjByKey(tempObj, key);
                outputObj[key] = foundObj;
            });

            output[element.groups.name] = outputObj;
        }
    }
    fs.writeFile('output.json', JSON.stringify(output, null, 1).replace(/{\s*"_text":(.*?)\s*}/gm,'$1'), (error) => { //RegEx entfernt das überflüssige _text Element 
        if (error) throw error;
        console.log('JSON wurde gespeichert!');
    });
}