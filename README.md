# IP_Chatbot
Ein Chatbot-Projekt basierend auf Rasa Open Source und MongoDB

## Rasa Projekt in Betrieb nehmen:

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
