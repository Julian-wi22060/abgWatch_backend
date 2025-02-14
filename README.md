# abgWatch_backend

## Einführung
Das **abgWatch_backend** ist ein Backend-Dienst, der API-Endpunkte bereitstellt, um Daten des Bundestages zu 
Abstimmungen und Mandatsträgern zu verwalten. Es verwendet eine modulare Struktur mit klar getrennten 
Verantwortlichkeiten für Datenbankverbindung, Logik und Tests. Das Backend ist Teil des docker-compose builds.

## Projektstruktur
```plaintext
abgWatch_backend/
├── Dockerfile                      # Docker-Konfiguration für das Deployment
├── README.md                       # Dokumentation des Backends
├── src/
│   ├── main.py                     # Startet den API-Server
│   ├── requirements.txt            # Enthält Abhängigkeiten für das Projekt
│   ├── helper/
│   │   ├── __init__.py
│   │   ├── db_connection.py        # Verwaltung der Datenbankverbindung
│   │   ├── v_candidacy_mandates.py # Verwaltung von Mandatsträgern
│   │   ├── vote_poll_details.py    # Verarbeitung von Abstimmungen
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_apis.py            # Enthält Testfälle für die APIs
```

## Tests ausführen
Das Projekt enthält automatische Tests zur Überprüfung der API-Funktionalität. <br>
Im Verzeichnis 'src' diesen Befehl ausführen:
```bash
python3 -m unittest tests/test_apis.py
```

## Detaillierte Modulbeschreibung
### `src/main.py`
Startpunkt der Anwendung, der API-Endpunkte definiert und Module aus `helper/` verwendet.

### `src/requirements.txt`
Listet alle benötigten Python-Bibliotheken auf, die mit `pip install -r requirements.txt` installiert werden können.

### `src/helper/`
- **`db_connection.py`**: Stellt die Verbindung zur Datenbank her und verwaltet Abfragen.
- **`v_candidacy_mandates.py`**: Enthält Logik zur Verwaltung von Mandatsträgern.
- **`vote_poll_details.py`**: Verwaltet Daten zu Abstimmungen im Bundestag.

### `src/tests/`
- **`test_apis.py`**: Enthält automatisierte Tests für die API-Endpunkte zur Validierung der Funktionalität.
