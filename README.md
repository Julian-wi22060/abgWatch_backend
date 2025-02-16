# Servicebeschreibung

Das **abgWatch_backend** stellt eine API bereit, die Daten zu Wahlumfragen, Kandidaturen und Mandaten verarbeitet und
zur Verfügung stellt. Es verwendet eine **modulare Architektur**, um Daten effizient zu verwalten. Das Backend ist Teil 
des docker-compose builds.


## Backend-Modul

Das Backend besteht aus mehreren Komponenten zur Verwaltung von API-Endpunkten und der Datenbankverbindung.
Diese Komponenten arbeiten zusammen, um eine robuste Datenverarbeitung zu gewährleisten.

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

## Komponenten des Backend-Moduls

### 1. **Hauptanwendung**
- **Datei:** `main.py`
- **Funktion:** Startet die API und verarbeitet eingehende Anfragen
- **Details:**
  - Implementiert die zentrale Logik zur Verwaltung von API-Endpunkten
  - Ruft Methoden aus den Modulen auf, um Daten zu verarbeiten
- **Wichtige Methoden:**
  - `create_app()`: Initialisiert und startet die API

### 2. **Datenbankverbindung**
- **Datei:** `db_connection.py`
- **Funktion:** Stellt die Verbindungsparameter zur Datenbank zur Verfügung
- **Details:**
  - Nutzt Umgebungsvariablen aus der docker-compose für die Datenbankverbindung und Authentifizierung
- **Wichtige Methoden:**
  - `get_db_connection()`: Beinhaltet die Umgebungsvariablen für die Datenbankverbindung

### 3. **Kandidatur- und Mandatsverwaltung**
- **Datei:** `v_candidacy_mandates.py`
- **Funktion:** Verarbeitet und verwaltet Informationen zu Kandidaturen und Mandaten.
- **Details:**
  - Stellt Methoden zum Abrufen und Strukturieren relevanter Daten über Mandatsträger im Bundestag bereit.
- **Wichtige Methoden:**
  - `get_v_candidacy_mandates()`: Ruft eine Liste aller Kandidaturen ab. Kann mit dem Query-Parameter grouped
  unterschiedliche Aggregationen ausgeben
  - `custom_json_serializer(obj)`: Benutzerdefinierte Serializer-Funktion, um beispielsweise 'Date' im ISO-Format zu erhalten

### 4. **Verwaltung von Wahlumfragen**
- **Datei:** `vote_poll_details.py`
- **Funktion:** Verwaltung und Bereitstellung von Abstimmungsdetails.
- **Details:**
  - Stellt Methoden zum Abrufen und Strukturieren relevanter Abstimmungen im Bundestag bereit.
- **Wichtige Methoden:**
  - `get_vote_poll_details()`: Gibt eine Liste aller erfassten Abstimmungen zurück. Kann mit dem Query-Parameter grouped
  unterschiedliche Aggregationen ausgeben
  - `custom_json_serializer(obj)`: Benutzerdefinierte Serializer-Funktion, um beispielsweise 'Date' im ISO-Format zu erhalten

## Funktionsweise des Backend-Moduls

1. **API-Server:** `main.py` startet die API und verwaltet die Endpunkte
2. **Datenbankverbindung:** `db_connection.py` stellt die Verbindungsparameter zur Verfügung, um diese anschließend in `vote_poll_details.py` oder `v_candidacy_mandates.py` für die Datenbankverbindung aufzurufen
3. **Datenverwaltung:** `v_candidacy_mandates.py` und `vote_poll_details.py` ermöglichen den Zugriff auf spezifische Aggregationen von Daten mittels APIs

## Beispielablauf

- **Abstimmungsdetails abrufen:**
  1. Eine Anfrage wird an den API-Endpunkt `/vote_poll_details` gesendet
  2. `vote_poll_details.py` verarbeitet die Anfrage und ruft Daten aus der Datenbank ab
  3. Die Daten werden formatiert und als JSON an den Client zurückgesendet

## Vorteile

- **Modularität:** Klare Trennung der Backend-Funktionalitäten für einfache Wartung
- **Flexibilität:** Unterstützt mehrere Datenquellen und API-Endpunkte

## Tests ausführen
Das Backend enthält automatisierte Tests zur Überprüfung der API-Funktionalitäten

### Testen mit unittest im Verzeichnis "src":
```bash
python3 -m unittest tests/test_apis.py
```

### Testfälle:
- **API-Verfügbarkeit:** Überprüft, ob der Server erreichbar ist.
- **Datenabruf:** Testet, ob API-Endpunkte korrekte Daten zurückgeben.
- **Datenbankabfragen:** Stellt sicher, dass SQL-Abfragen korrekt ausgeführt werden.
- Dies wird getestet anhand aller APIs:
  - /v_candidacy_mandates/ 
  - /v_candidacy_mandates/?grouped=1 
  - /v_candidacy_mandates/?grouped=2
  - /vote_poll_details/
  - /vote_poll_details/?grouped=1 
  - /vote_poll_details/?grouped=2
