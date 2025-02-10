# Lernassistent

## Projektübersicht

Dieses Projekt ist ein Lernassistent, der verschiedene Dienste bereitstellt, um das Lernen zu erleichtern. Es umfasst mehrere Microservices, die in Docker-Containern ausgeführt werden.

## Verzeichnisstruktur

- `Services/Anki`: Enthält den Anki-Karten-Service.
- `View`: Enthält die Frontend-Dateien.
- `docker-compose.yml`: Docker Compose Datei zum Starten aller Dienste.

## Voraussetzungen

- Docker
- Docker Compose

## Installation

1. Klonen Sie das Repository:
    ```sh
    git clone https://github.com/magn4/Lernassistent.git
    cd Lernassistent
    ```

2. Erstellen Sie eine [.env](http://_vscodecontentref_/0) Datei im Stammverzeichnis und fügen Sie die folgenden Umgebungsvariablen hinzu:
    ```env
    DB_HOST=db
    DB_PORT=5432
    DB_NAME=lernassistent
    DB_USER=postgres
    DB_PASSWORD=yourpassword
    ```

3. Starten Sie die Docker-Container:
    ```sh
    docker-compose up --build
    ```

## Dienste

### Anki Karten Service

Der Anki Karten Service bietet Endpunkte zum Erstellen, Aktualisieren und Löschen von Anki-Karten und -Decks.

- **URL**: `http://localhost:8000`
- **Endpunkte**:
  - `POST /cards`: Erstellen einer neuen Karte
  - `PUT /decks/{deck_id}`: Aktualisieren eines Decks
  - `POST /files`: Öffnen einer Datei

### Nginx Reverse Proxy

Der Nginx-Container fungiert als Reverse Proxy für alle Dienste.

- **URL**: `http://localhost`

## Datenbank

Die PostgreSQL-Datenbank speichert alle Daten für den Lernassistenten.

- **Host**: `db`
- **Port**: `5432`
- **Datenbankname**: `lernassistent`
- **Benutzer**: `postgres`
- **Passwort**: `yourpassword`

## Health Checks

Die Docker-Compose-Datei enthält Health Checks für die Dienste, um sicherzustellen, dass sie ordnungsgemäß funktionieren.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen finden Sie in der `LICENSE`-Datei.