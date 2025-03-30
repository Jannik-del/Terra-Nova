import nextcord
from nextcord.ext import commands
import json
import os
from datetime import datetime
from config import LEAVE_CHANNEL_ID  # Stelle sicher, dass diese ID in deiner config.py definiert ist


class LeaveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leave_messages_file = "leave_logs.json"
        print("Leave is online.")

    def save_leave_log(self, user_id, username, timestamp):
        """Speichert die Informationen über den Benutzer, der den Server verlassen hat."""
        # Überprüfen, ob die Datei existiert, und sie erstellen, falls nicht
        if not os.path.exists(self.leave_messages_file):
            with open(self.leave_messages_file, "w") as f:
                json.dump([], f)

        # Bestehende Logs laden
        with open(self.leave_messages_file, "r") as f:
            logs = json.load(f)

        # Neuen Eintrag hinzufügen
        logs.append({
            "user_id": user_id,
            "username": username,  # Speichert "Benutzername#1234"
            "timestamp": timestamp
        })

        # Logs speichern
        with open(self.leave_messages_file, "w") as f:
            json.dump(logs, f, indent=4)

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        """Sendet eine Nachricht, wenn ein Benutzer den Server verlässt."""
        channel = self.bot.get_channel(LEAVE_CHANNEL_ID)
        if channel:
            # Nachricht im Kanal senden
            leave_embed = nextcord.Embed(
                title="Abschied 👋",
                description=f"{member} hat den Server verlassen.",  # Zeigt "Benutzername#1234"
                color=nextcord.Color.red()
            )
            leave_embed.set_footer(text=f"Benutzer-ID: {member.id}")
            leave_embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            await channel.send(embed=leave_embed)

            # Log speichern
            timestamp = datetime.utcnow().isoformat()
            self.save_leave_log(member.id, str(member), timestamp)  # Speichert "Benutzername#1234"
        else:
            print(f"Kanal mit der ID {LEAVE_CHANNEL_ID} nicht gefunden.")

    @nextcord.slash_command(name="leave_logs", description="Zeigt die Logs von Benutzern, die den Server verlassen haben.")
    @commands.has_any_role(1352254181305618495)
    async def leave_logs(self, interaction: nextcord.Interaction):
        """Slash-Befehl, um die Logs von verlassenen Benutzern anzuzeigen."""
        # Überprüfen, ob Logs existieren
        if not os.path.exists(self.leave_messages_file):
            await interaction.response.send_message("Es gibt keine Leave-Logs.", ephemeral=True)
            return

        # Logs laden
        with open(self.leave_messages_file, "r") as f:
            logs = json.load(f)

        if not logs:
            await interaction.response.send_message("Es gibt keine Leave-Logs.", ephemeral=True)
            return

        # Erstelle eine übersichtliche Log-Ausgabe
        logs_message = "\n".join(
            f"- {log['username']} (ID: {log['user_id']}) am {log['timestamp']}" for log in logs
        )
        await interaction.response.send_message(f"**Leave Logs:**\n{logs_message}", ephemeral=True)


def setup(bot):
    if bot.get_cog("LeaveCog") is None:
        bot.add_cog(LeaveCog(bot))