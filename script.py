import os
import time
import logging
import keyring
from keyrings.alt.file import PlaintextKeyring
from pyicloud import PyiCloudService
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Keyring auf Dateisystem setzen
keyring.set_keyring(PlaintextKeyring())

# Schwellenwert für Positionsänderung (in Dezimalgrad)
CHANGE_THRESHOLD = 0.0001

# Datenbankverbindung prüfen
def connect_to_database():
    while True:
        try:
            db = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            if db.is_connected():
                logging.info("Erfolgreich mit der Datenbank verbunden.")
                return db
        except Error as e:
            logging.error(f"Fehler beim Verbinden zur Datenbank: {e}")
            logging.info("Erneuter Verbindungsversuch in 5 Sekunden...")
            time.sleep(5)

# Funktion zur Überprüfung der Positionsänderung
def has_significant_change(last_lat, last_lon, new_lat, new_lon):
    return abs(last_lat - new_lat) > CHANGE_THRESHOLD or abs(last_lon - new_lon) > CHANGE_THRESHOLD

# iCloud-Verbindung herstellen
icloud = PyiCloudService(
    os.getenv('ICLOUD_EMAIL'),
    os.getenv('ICLOUD_PASSWORD'),
    cookie_directory='/root/.local/share/python_keyring'
)

# Zwei-Faktor-Authentifizierung
if icloud.requires_2fa:
    code = os.getenv('ICLOUD_2FA_CODE')
    if not code:
        logging.error("Zwei-Faktor-Authentifizierung erforderlich. Kein Code gefunden.")
        sys.exit(1)

    result = icloud.validate_2fa_code(code)
    if not result:
        logging.error("Ungültiger Zwei-Faktor-Code.")
        sys.exit(1)
    logging.info("Zwei-Faktor-Authentifizierung erfolgreich.")

if icloud.requires_2fa and not icloud.is_trusted_session:
    logging.error("Vertrauenswürdige Sitzung erforderlich.")
    sys.exit(1)

# Datenbankverbindung herstellen
db = connect_to_database()
cursor = db.cursor()

# Tabelle erstellen, falls sie nicht existiert
cursor.execute("""
    CREATE TABLE IF NOT EXISTS device_locations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        device_name VARCHAR(255),
        latitude DOUBLE,
        longitude DOUBLE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

# Endlosschleife für die Abfrage alle 10 Minuten
try:
    while True:
        # Standortdaten von Geräten abrufen
        devices = icloud.devices
        for device in devices:
            location = device.location()
            if location:
                device_name = device['name']
                latitude = location['latitude']
                longitude = location['longitude']
                timestamp = datetime.fromtimestamp(location['timeStamp'] / 1000)

                # Letzten Eintrag abrufen
                cursor.execute("""
                    SELECT latitude, longitude FROM device_locations
                    WHERE device_name = %s
                    ORDER BY timestamp DESC LIMIT 1
                """, (device_name,))
                last_entry = cursor.fetchone()

                # Nur einfügen, wenn sich die Position signifikant geändert hat
                if last_entry is None or has_significant_change(last_entry[0], last_entry[1], latitude, longitude):
                    logging.info(f"Gerät: {device_name}, Latitude: {latitude}, Longitude: {longitude}, Zeit: {timestamp}")
                    cursor.execute("""
                        INSERT INTO device_locations (device_name, latitude, longitude, timestamp)
                        VALUES (%s, %s, %s, %s)
                    """, (device_name, latitude, longitude, timestamp))
                else:
                    logging.info(f"Keine signifikante Positionsänderung für {device_name}. Eintrag übersprungen.")

        # Änderungen speichern
        db.commit()

        # 10 Minuten warten
        logging.info("Warten auf die nächste Abfrage in 10 Minuten...")
        time.sleep(600)

except KeyboardInterrupt:
    logging.info("Skript manuell beendet.")

finally:
    cursor.close()
    db.close()
