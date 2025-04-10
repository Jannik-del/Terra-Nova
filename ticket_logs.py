import json
import os
from datetime import datetime
import pytz

# Ordner für die Ticket-Logs
LOGS_DIRECTORY = "ticket_logs"

# Stelle sicher, dass der Ordner existiert
os.makedirs(LOGS_DIRECTORY, exist_ok=True)

# Ticket-Logs speichern
async def save_ticket_logs(channel, ticket_type):
    try:
        # Nachrichten aus dem Kanal abrufen
        print("Hole Nachrichten aus dem Kanal...")
        messages = [msg async for msg in channel.history(limit=100)]
        berlin_tz = pytz.timezone('Europe/Berlin')

        # Nachrichten in ein Dictionary formatieren
        print(f"Verarbeite {len(messages)} Nachrichten...")
        message_data = [
            {
                "content": msg.content,
                "author": str(msg.author),
                "timestamp": msg.created_at.astimezone(berlin_tz).strftime('%d-%m-%Y %H:%M:%S')
            }
            for msg in reversed(messages)
        ]

        # Ticket-Daten erstellen
        ticket_data = {
            "ticket_name": str(channel.name),
            "ticket_type": ticket_type,
            "created_at": datetime.now(berlin_tz).strftime('%d-%m-%Y %H:%M:%S'),
            "messages": message_data,
        }

        # JSON-Dateiname basierend auf Benutzername, Ticket-Typ und Datum
        user_name = channel.name.split("-")[0]
        timestamp = datetime.now(berlin_tz).strftime('%d-%m-%Y_%H-%M-%S')
        file_name = f"{user_name}_{ticket_type}_{timestamp}.json"
        file_path = os.path.join(LOGS_DIRECTORY, file_name)

        print(f"Speichere Ticket-Logs in {file_path}...")

        # Ticket-Logs in der Datei speichern
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(ticket_data, file, indent=4, ensure_ascii=False)

        print(f"Ticket-Logs gespeichert in: {file_path}")

    except Exception as e:
        print(f"Fehler beim Speichern der Ticket-Logs: {e}")
