Erstes Treffen


- Gestaltungsrichtlinien Kreis Wesel, am Farbkonzept orientieren
	-  Konkrete Gestaltungsvorgaben?


- Intuitive Bedienbarkeit
	- Altersgruppe der Benutzer google analytics + alter der Anrufer


- Soll Fragen beantworten können
    Auf Keywords achten
    achten auf Synonyme oder umgangssprachliche Verwaltungsbegriffe
    sowie der Wissensdatenbank des Kreisservicecenters 
	- Umfang der häufig gestellten Fragen und die eher selten gestellten Fragen (FAQ?)


- Spätere Erweiterung um neue oder veränderte Leistungen muss möglich sein
Nutzbarkeit sowohl in der aktuellen Webpräsenz auf Basis Lotus
/KRZN E-Government-Suite als auch in der zukünftigen Lösung über
DRUPOLIS auf Basis von Drupal
	- Framework basierend auf konkrete Komplexität (wird später entschieden)


Anforderungen

    1. Verständnis der Anforderungen
    2. Kozepterstellung
    3. Nutzersicht liegt im Vordergrund
    4. Kreativität bei Erstellung und Namensgebung



Vorbereitung 1. Treffen: 
    - Storyboard/HTML-Prototyp für Nutzerbeispiele


Vorbereitung 2. Treffen:

    - Zusammenfassung der Prototypen als ein gemeinsamer Prototyp

    - Framework informieren


Neue Anforderungen:

    - was passiert nach dem Zuklappen, wenn noch eine Antwort abgewartet wird

    - schließen per "X" oder Button unten links

    - FAQ als erste Botnachricht 

    - Email und Telefon oben - nach Klick als Chatbotantwort

    - Animation wenn auf eine Nachricht gewartet wird
    
    - Opacity ja/nein wenn ja wie soll die farbe angepasst werden


Fragen für 19.11.2020:

    - was passiert nach dem Zuklappen, wenn noch eine Antwort abgewartet wird (Toast o.ä.)

    - Verlinkung zu einer FAQ-Seite ?

    - E-Mail als Mailto oder als Link zu Kontakt-Formular


Rasa Projekt in Betrieb nehmen HowTo:

    - python3 -m venv ./venv (falls noch kein virtuelles Environment erstellt wurde)
    - source ./venv/bin/activate (virtuelle Umgebung "betreten")

wenn rasa noch nicht installiert wurde

    - pip3 install -U pip3
    - pip3 install rasa

    - rasa train (model trainieren)
    - rasa shell (test chat)
    - rasa shell nlp (nlp test für eingegebene Nachrichten)

Spacy installation

    - pip3 install rasa[spacy]
    - python3 -m spacy download de_core_news_md
    - python3 -m spacy link de_core_news_md de

um den Rasa Rest Channel zu starten

    - rasa run --cors "*"
