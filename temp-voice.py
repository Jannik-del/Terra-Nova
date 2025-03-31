import os
import nextcord
import config
from nextcord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
import json

class TempVoice(commands.Cog):
    def __init__(self, client):
        print("Temp voice is online.")
        self.client = client
        
        # Pfad zur Log-Datei in einem Ordner
        self.log_folder = "logs_temp_vc"
        self.log_file = os.path.join(self.log_folder, "temp_voice_logs.json")
        
        # Ordner erstellen, falls er nicht existiert
        os.makedirs(self.log_folder, exist_ok=True)
        
        self.voice_channels = {}  # Speichert temporäre Voice-Channel
        self.load_logs()

    def log(self, message: str):
        """Hilfsfunktion für Konsolenausgaben mit Timestamp."""
        timestamp = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
        print(f"{timestamp} {message}")

    def load_logs(self):
        """Lade bestehende Logs aus der JSON-Datei."""
        try:
            with open(self.log_file, "r") as file:
                self.logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.logs = {}  # Leere Logs, falls keine Datei existiert oder ungültig ist

    def save_logs(self):
        """Speichere die Logs in der JSON-Datei."""
        with open(self.log_file, "w") as file:
            json.dump(self.logs, file, indent=4)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Erstelle oder aktualisiere temporäre Voice-Channel."""
        
        # Benutzer betritt einen Channel
        if after.channel and not before.channel:
            join_channel = after.channel
            target_channel_id = 1352254182014582796

            # Überprüfe, ob der Benutzer dem Trigger-Channel beigetreten ist
            if join_channel.id == target_channel_id:
                self.log(f"{member.name} ist dem Trigger-Channel '{join_channel.name}' beigetreten.")
                
                # Kategorie für temporäre Voice-Channels
                category_name = "🎙| voice"
                category = nextcord.utils.get(member.guild.categories, name=category_name)
                if not category:
                    category = await member.guild.create_category(name=category_name)
                    self.log(f"Kategorie '{category_name}' wurde erstellt.")

                # Erstelle einen temporären Voice-Channel
                temp_channel = await category.create_voice_channel(name=f"Temp-{member.name}")
                self.log(f"Temporärer Channel '{temp_channel.name}' wurde erstellt.")
                
                # Verschiebe den Benutzer in den neuen Channel
                await member.move_to(temp_channel)
                self.log(f"{member.name} wurde in den Channel '{temp_channel.name}' verschoben.")

                # Speichere Channel-Informationen und Logs
                self.voice_channels[temp_channel.id] = {
                    "owner": member.id,
                    "creation_time": datetime.utcnow(),
                    "channel": temp_channel
                }
                self.logs[temp_channel.id] = {
                    "channel_name": temp_channel.name,
                    "created_by": member.name,
                    "created_at": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"),
                    "members": [],
                    "deleted_at": None
                }
                self.save_logs()

                # Überwache den Channel
                await self.monitor_channel(temp_channel)

            # Logge, wenn ein Benutzer einem bestehenden temporären Channel beitritt
            elif join_channel.id in self.voice_channels:
                self.log(f"{member.name} ist dem Channel '{join_channel.name}' beigetreten.")
                channel_id = join_channel.id
                self.logs[channel_id]["members"].append({
                    "user": member.name,
                    "action": "joined",
                    "timestamp": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
                })
                self.save_logs()

        # Benutzer verlässt einen Channel
        if before.channel and before.channel.id in self.voice_channels:
            self.log(f"{member.name} hat den Channel '{before.channel.name}' verlassen.")
            channel_id = before.channel.id
            self.logs[channel_id]["members"].append({
                "user": member.name,
                "action": "left",
                "timestamp": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
            })
            self.save_logs()

    async def monitor_channel(self, channel):
        """Überwacht temporäre Voice-Channels und löscht sie nach 4 Tagen oder wenn leer."""
        while True:
            await asyncio.sleep(5)  # Alle 5 Sekunden überprüfen

            # Wenn der Channel leer ist, lösche ihn
            if len(channel.members) == 0:
                await channel.delete()
                self.log(f"Channel '{channel.name}' wurde gelöscht, da er leer war.")

                # Aktualisiere die Logs
                channel_id = channel.id
                self.logs[channel_id]["deleted_at"] = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
                self.save_logs()

                # Entferne den Channel aus der internen Liste
                del self.voice_channels[channel_id]
                break

            # Lösche den Channel nach 4 Tagen
            elapsed_time = datetime.utcnow() - self.voice_channels[channel.id]["creation_time"]
            if elapsed_time >= timedelta(days=4):
                await channel.delete()
                self.log(f"Channel '{channel.name}' wurde nach 4 Tagen gelöscht.")

                # Aktualisiere die Logs
                channel_id = channel.id
                self.logs[channel_id]["deleted_at"] = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
                self.save_logs()

                # Entferne den Channel aus der internen Liste
                del self.voice_channels[channel_id]
                break

def setup(client):
    client.add_cog(TempVoice(client))