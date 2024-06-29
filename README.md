# iCloud Device Tracker

Dieses Projekt ermöglicht das Tracking von Geräten, Personen und Objekten über die Apple "Wo ist?"-Funktion und speichert die Standortdaten in einer MariaDB-Datenbank.

## Inhaltsverzeichnis

- [Installation](#installation)
- [Verwendung](#verwendung)
- [Umgebungsvariablen](#umgebungsvariablen)
- [Docker-Setup](#docker-setup)
- [Technologien](#technologien)
- [Lizenz](#lizenz)

## Installation

1. **Repository klonen**:

   ```bash
   git clone https://github.com/dein-benutzername/icloud-device-tracker.git
   cd icloud-device-tracker
   ```

2. **.env Datei erstellen**:

   Erstelle eine `.env`-Datei im Stammverzeichnis und füge die folgenden Umgebungsvariablen hinzu:

   ```env
   ICLOUD_EMAIL=your_email@example.com
   ICLOUD_PASSWORD=your_password
   ICLOUD_2FA_CODE=your_2fa_code
   DB_HOST=mariadb
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=wo_ist
   ```

3. **Docker-Container bauen und starten**:

   ```bash
   docker-compose up --build
   ```

## Verwendung

- Starte das Projekt mit dem Befehl `docker-compose up --build`.
- Die Standortdaten werden in der Konsole angezeigt und in der MariaDB-Datenbank gespeichert.

## Umgebungsvariablen

- **ICLOUD_EMAIL**: Deine iCloud-E-Mail-Adresse.
- **ICLOUD_PASSWORD**: Dein iCloud-Passwort.
- **ICLOUD_2FA_CODE**: Zwei-Faktor-Authentifizierungscode für iCloud.
- **DB_HOST**: Hostname des MariaDB-Dienstes.
- **DB_USER**: Benutzername für die MariaDB-Datenbank.
- **DB_PASSWORD**: Passwort für die MariaDB-Datenbank.
- **DB_NAME**: Name der MariaDB-Datenbank.

## Docker-Setup

- **`Dockerfile`**: Enthält die Anweisungen zum Erstellen des Docker-Images.
- **`docker-compose.yml`**: Definiert die Dienste, Volumes und Umgebungsvariablen.
- **`requirements.txt`**: Listet alle Python-Abhängigkeiten auf, einschließlich `pyicloud`, `mysql-connector-python` und `keyrings.alt`.

## Technologien

- **Python**: Backend-Programmiersprache.
- **MariaDB**: Relationale Datenbank zur Speicherung von Standortdaten.
- **Docker**: Containerisierungstechnologie zur Verwaltung der Anwendungsumgebung.
- **ICloud**: Schnittstelle zur Apple "Wo ist?"-Funktion.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

---

### Hinweise

- Stelle sicher, dass du alle erforderlichen Berechtigungen hast, um auf iCloud-Daten zuzugreifen.
- Die Verwendung von `keyrings.alt` speichert Passwörter im Klartext. In Produktionsumgebungen sollten sicherere Alternativen verwendet werden.
