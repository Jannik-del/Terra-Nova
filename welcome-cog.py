import json
import os
import nextcord
from nextcord.ext import commands
from config import WELCOME_CHANNEL_ID


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_log_file = "welcome_messages.json"

    def save_message_id(self, user_id, message_id):
        """Speichert die Nachricht-ID für einen Benutzer."""
        if not os.path.exists(self.message_log_file) or os.path.getsize(self.message_log_file) == 0:
            with open(self.message_log_file, "w") as f:
                json.dump({}, f)

        with open(self.message_log_file, "r") as f:
            data = json.load(f)

        timestamp = nextcord.utils.utcnow().strftime('%d-%m-%Y %H:%M:%S')  # Zeitstempel im gewünschten Format
        data[str(user_id)] = {"message_id": message_id, "timestamp": timestamp}

        with open(self.message_log_file, "w") as f:
            json.dump(data, f, indent=4)

    def delete_message_id(self, user_id):
        """Löscht die Nachricht-ID für einen Benutzer."""
        if os.path.exists(self.message_log_file):
            with open(self.message_log_file, "r") as f:
                data = json.load(f)

            data.pop(str(user_id), None)

            with open(self.message_log_file, "w") as f:
                json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        """Event: Wird ausgelöst, wenn ein neuer Benutzer dem Server beitritt."""
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            embed = nextcord.Embed(
                title="Willkommen!",
                description=(
                    f"Hallo {member.mention}, willkommen auf unserem Server! 🎉\n"
                    "Wir freuen uns, dich hier zu haben."
                ),
                color=nextcord.Color.green(),
            )
            view = WelcomeView(member)  # Neues Mitglied übergeben
            message = await channel.send(embed=embed, view=view)
            self.save_message_id(member.id, message.id)

    @nextcord.slash_command(name="test-welcome", description="Testet die Willkommensnachricht.")
    @commands.has_any_role(1352254181305618495, 1352254181297094695, 1352254181297094692)
    async def test_welcome(self, interaction: nextcord.Interaction):
        """Test-Befehl, um die Willkommensnachricht zu simulieren."""
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            test_member = interaction.user  # Verwende den Benutzer, der den Befehl ausführt
            embed = nextcord.Embed(
                title="Willkommen! (Test)",
                description=(
                    f"Hallo {test_member.mention}, willkommen auf unserem Server! 🎉\n"
                    "Dies ist eine Testnachricht."
                ),
                color=nextcord.Color.blue(),
            )
            view = WelcomeView(test_member)
            message = await channel.send(embed=embed, view=view)
            self.save_message_id(test_member.id, message.id)
            await interaction.response.send_message(
                "Die Willkommensnachricht wurde erfolgreich getestet!", ephemeral=True
            )


class WelcomeView(nextcord.ui.View):
    def __init__(self, member: nextcord.Member):
        super().__init__(timeout=None)
        self.member = member

    @nextcord.ui.button(label="Begrüßen", style=nextcord.ButtonStyle.success, custom_id="welcome_greet")
    async def greet_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Button: Sendet eine Nachricht, dass ein Benutzer den neuen begrüßt hat."""
        await interaction.response.send_message(
            f"{interaction.user.mention} hat {self.member.mention} auf dem Server begrüßt! 🎉",
            ephemeral=False,
        )


def setup(bot):
    bot.add_cog(WelcomeCog(bot))
