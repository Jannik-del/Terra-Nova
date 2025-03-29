import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from datetime import datetime

class ServerStatsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Serverstats Befehl, um Informationen über den Server anzuzeigen
    @nextcord.slash_command(name="user_info", description="Zeige Informationen über einen Benutzer an.")
    async def user_info(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = SlashOption(name="user", description="Wähle einen Benutzer", required=True)
    ):
        # Benutzerinformationen sammeln
        name = f"{user.display_name} | {user.name}#{user.discriminator}"
        user_id = user.id
        created_at = user.created_at.strftime("%d. %B %Y")
        joined_at = user.joined_at.strftime("%d. %B %Y")
        roles = [role.mention for role in user.roles[1:]]  # Rolle @everyone ignorieren

        # Embed erstellen
        embed = nextcord.Embed(color=0x2F3136)
        embed.set_author(name="Verzweiflung3.0", icon_url=self.client.user.avatar.url)
        embed.add_field(name="✨ Name", value=name, inline=False)
        embed.add_field(name="🆔 ID", value=user_id, inline=False)
        embed.add_field(name="📅 Created", value=f"{created_at} | vor {datetime.now().year - user.created_at.year} Jahren", inline=False)
        embed.add_field(name="🏠 Joined Server", value=f"{joined_at} | vor {datetime.now().year - user.joined_at.year} Jahren", inline=False)
        embed.add_field(name="🔒 Roles", value=" ".join(roles) if roles else "Keine Rollen", inline=False)

        # Avatar hinzufügen
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)

        await interaction.response.send_message(embed=embed)

        try:
            embed.set_thumbnail(url=guild.icon.url if guild.icon else None)  # Server-Icon, falls vorhanden
            embed.set_footer(text=f"Angefragt von {interaction.user.name}", icon_url=interaction.user.avatar.url)
        except:
            pass

        try:
            await interaction.response.send_message(embed=embed)
        except:
            pass

def setup(client):
    client.add_cog(ServerStatsCog(client))