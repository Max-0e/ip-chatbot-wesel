Rasa Projekt in Betrieb nehmen HowTo:

    `python3 -m venv ./venv` (falls noch kein virtuelles Environment erstellt wurde)
    `source ./venv/bin/activate` (virtuelle Umgebung "betreten")

wenn rasa noch nicht installiert wurde

    `pip3 install -U pip3`
    `pip3 install rasa`

    - `rasa train` (model trainieren)
    - `rasa shell` (test chat)
    - `rasa shell nlp` (nlp test für eingegebene Nachrichten)

Spacy installation

    - `pip3 install rasa[spacy]`
    - `python3 -m spacy download de_core_news_md`
    - `python3 -m spacy link de_core_news_md de`

um den Rasa Rest Channel zu starten

    - `rasa run --cors "*"`

mongoDb unter Ubuntu starten

    - `sudo systemctl start mongod`
