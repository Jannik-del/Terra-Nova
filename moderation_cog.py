import nextcord
from nextcord.ext import commands
from datetime import timedelta

class ModerationCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="timeout", description="Setze einen Benutzer in den Timeout.")
    @commands.has_permissions(administrator=True)
    @commands.has_any_role(1352254181305618495, 1352254181297094693,) #orga #Mod-Team
    async def timeout(self, interaction: nextcord.Interaction, user: nextcord.Member, minutes: int, reason: str = None):
        try:
            timeout_duration = timedelta(minutes=minutes)
            await user.timeout(timeout_duration, reason=reason)
            await interaction.response.send_message(f"{user.mention} wurde für {minutes} Minuten in den Timeout gesetzt.")
        except nextcord.Forbidden:
            await interaction.response.send_message("Ich habe keine Berechtigung, diesen Benutzer in den Timeout zu setzen.", ephemeral=True)
        except nextcord.HTTPException as e:
            await interaction.response.send_message(f"Fehler beim Timeout: {e.status} - {e.text}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Ein unbekannter Fehler ist aufgetreten: {str(e)}", ephemeral=True)


    # Nur Benutzer mit der Rolle "Admin" oder "Moderator" können diesen Befehl ausführen
    @nextcord.slash_command(name="kick", description="Kicke einen Benutzer vom Server.")
    @commands.has_permissions(administrator=True)
    @commands.has_any_role(1352254181305618495, 1353466748854079589,) #orga #Special-Mod-Team
    async def kick(self, interaction: nextcord.Interaction, user: nextcord.Member, reason: str = None):
        await interaction.guild.kick(user, reason=reason)
        await interaction.response.send_message(f"{user.mention} wurde vom Server gekickt.")

    @kick.error
    async def kick_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, commands.MissingRole):
            await interaction.response.send_message("Du hast nicht die erforderliche Rolle, um diesen Befehl zu verwenden.", ephemeral=True)



    # Nur Benutzer mit der Rolle "Admin" können diesen Befehl ausführen
    @nextcord.slash_command(name="ban", description="Banne einen Benutzer.")
    @commands.has_permissions(administrator=True)
    @commands.has_any_role(1352254181305618495,)
    async def ban(self, interaction: nextcord.Interaction, user: nextcord.Member, reason: str = None):
        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(f"{user.mention} wurde gebannt.")

    # Fehlerbehandlung, falls der Benutzer nicht die erforderliche Rolle hat
    @ban.error
    async def ban_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, commands.MissingRole):
            await interaction.response.send_message("Du hast nicht die erforderliche Rolle, um diesen Befehl zu verwenden.", ephemeral=True)

def setup(client):
    client.add_cog(ModerationCog(client))