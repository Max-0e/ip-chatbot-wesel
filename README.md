# IP_Chatbot
Ein Chatbot-Projekt basierend auf Rasa Open Source und MongoDB

## Rasa Projekt in Betrieb nehmen:

`git clone https://gitlab.hsrw.eu/maximilian.oedinger/ip-chatbot-wesel.git`

`cd ip-chatbot-wesel`

`mkdir rasa/models`

`python3 -m venv ./venv` (falls noch kein virtuelles Environment erstellt wurde)

`source ./venv/bin/activate` (virtuelle Umgebung "betreten")


### Rasa installation in der virtuellen Umgebung

`pip3 install -U pip3`

`pip3 install rasa`


##### Spacy installation

`pip3 install rasa[spacy]`

`python3 -m spacy download de_core_news_md`

`python3 -m spacy link de_core_news_md de`



## Überblick: Rasa CLI-Befehle

`rasa train` (model trainieren)

`rasa shell` (test chat)

`rasa shell nlp` (nlp test für eingegebene Nachrichten)

`rasa run --cors "*"` (Rasa Rest Channel starten)

`rasa run actions`(Action-Server starten)


### mongoDb unter Ubuntu starten

`sudo systemctl start mongod`

## Rasa X

`pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple`

`rasa x`


## Welche Bereiche/Themen soll der Bot abdecken?

Dafür wurden uns vom Kreis Wesel zur Verfügung gestellte Excel-Tabellen mit Besuchsstatistiken analysiert

Bereiche und Seiten mit vielen Besuchen (Klickzahlen > 3000 (in Bereichen jeweils absteigend)):

**Allgemeine Informationen** <br>
    -Willkommen <br>
    -Suchergebnisse <br>
    -Kreis & Verwaltung <br>
    -Öffnungszeiten <br>
    -Themen A-Z <br>
    -Service <br>
    -Tipps und Termine <br>
    -Kontakt <br>
    -Kreisverwaltung <br>
    -Dienstleistungen <br>
    -Presse <br>
    -Online-Dienste <br>
    -Impressum <br>
    -Aktuelles <br>

**KFZ** <br>
    -Zulassungsangelegenheiten <br>
    -Wunschkennzeichen <br>
    -Auto, Führerschein und Straßenverkehr <br>
    -Internetzulassung / i-KFZ <br>
    -Führerscheinangelegenheiten <br>
    -36-1-3 Zulassungs- und Führerscheinservice <br>
    -Fahrzeug - Abmeldung <br>

**Jobs** <br>
    -Stellenangebote <br>
    -Job und Karriere <br>
    -Info-Portal Personalangelegenheiten <br>

**Familiäres** <br>
    -Elterngeld <br>
    -Kinder, Jugend, Familie <br>
    -Elternbeiträge <br>
    -KITA ONLINE <br>
    -Schulamt für den Kreis Wesel <br>

**Lehre** <br>
    -Belehrung für den Umgang mit Lebensmitteln <br>
    -Terminbuchung: Belehrung nach dem Infektionsschutzgesetz <br>

**Diverses** <br>
    -Schwerbehindertenausweise <br>
    -Ausländerangelegenheiten <br>
    -10 Top-Touren im Kreis Wesel <br>

## (Vorläufiges) Fazit

Gerade allgemeine Informationen über den Kreis und seine Einrichtungen sowie das Thema KFZ stechen als außerordentlich beliebte Themen hervor und sollten Priorität erhalten. Daneben erfreuen sich die Bereiche "Jobs" und vor allem auch alles rund um die Familie großer Beliebtheit.

