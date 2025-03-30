import nextcord
from nextcord.ext import commands
import os
import asyncio
import nacl  # PyNaCl wird benötigt für Voice-Funktionalität


class VoicePlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="play_audio", description="Spielt eine Audio-Datei im Voice-Channel ab.")
    @commands.has_any_role(1352254181305618495, 1352254181297094695, 1352254181297094692)
    async def play_audio(self, interaction: nextcord.Interaction, audio_file: str):
        """Slash Command: Spielt eine Audiodatei im Voice-Channel ab."""
        # Überprüfen, ob der Nutzer in einem Voice-Channel ist
        if not interaction.user.voice:
            await interaction.response.send_message("Du bist in keinem Voice-Channel!", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel

        # Überprüfen, ob die Datei existiert
        audio_path = f"./audio/{audio_file}"
        if not os.path.exists(audio_path):
            await interaction.response.send_message(f"Die Datei `{audio_file}` existiert nicht im Ordner `audio`.",
                                                    ephemeral=True)
            return

        # Bot tritt dem Voice-Channel bei
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(voice_channel)
        else:
            voice_client = await voice_channel.connect()

        # Audiodatei abspielen mit PyNaCl
        try:
            audio_source = nextcord.PCMAudio(audio_path)  # PyNaCl-basierte Wiedergabe
            voice_client.play(audio_source, after=lambda e: print(f"Audio-Fehler: {e}") if e else None)
            await interaction.response.send_message(f"Spiele die Datei `{audio_file}` in `{voice_channel.name}` ab.",
                                                    ephemeral=False)

            # Warte, bis die Wiedergabe abgeschlossen ist
            while voice_client.is_playing():
                await asyncio.sleep(1)
        except Exception as e:
            await interaction.followup.send(f"Fehler beim Abspielen der Datei: {e}", ephemeral=True)

    @nextcord.slash_command(name="leave", description="Der Bot verlässt den Voice-Channel.")
    async def leave(self, interaction: nextcord.Interaction):
        """Slash Command: Der Bot verlässt den Voice-Channel."""
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await interaction.response.send_message("Der Bot hat den Voice-Channel verlassen.", ephemeral=True)
        else:
            await interaction.response.send_message("Ich bin in keinem Voice-Channel verbunden.", ephemeral=True)

    @nextcord.slash_command(name="list_audio", description="Listet alle verfügbaren Audiodateien auf.")
    async def list_audio(self, interaction: nextcord.Interaction):
        """Slash Command: Listet alle Audiodateien im Ordner auf."""
        audio_folder = "./audio"
        if not os.path.exists(audio_folder):
            os.makedirs(audio_folder)

        audio_files = [f for f in os.listdir(audio_folder) if os.path.isfile(os.path.join(audio_folder, f))]
        if not audio_files:
            await interaction.response.send_message("Es sind keine Audiodateien verfügbar.", ephemeral=True)
        else:
            file_list = "\n".join(audio_files)
            await interaction.response.send_message(f"Verfügbare Audiodateien:\n```\n{file_list}\n```", ephemeral=True)


def setup(bot):
    bot.add_cog(VoicePlayer(bot))
