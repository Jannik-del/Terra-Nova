import nextcord
from nextcord.ext import commands
import config


class ServerInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="ip", description="Zeigt die IP des Servers an")
    async def server_ip(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="****Server IP****",
            description="**Hier ist die IP zum Joinen des Servers:**",
            color=nextcord.Color.purple()
        )
        embed.add_field(name="**Kommt vllt Irgend wann**", value="", inline=False)
        embed.set_footer(text="Verbinde dich jetzt!")
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="mc-info", description="Zeigt Infos des Servers an")
    async def server_info(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="****MC-Info****",
            description="**Infos zum Server**",
            color=nextcord.Color.blue()
        )
        embed.add_field(name="**INFOS HIER: ...**",
                        value="", inline=False)
        embed.set_footer(text="Don´t cheat")
        await interaction.response.send_message(embed=embed)


class CommandsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="test-response", description="Nur zum Testen")
    @commands.has_any_role(1352254181305618495, 1352254181305618494)
    async def test(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="Test erfolgreich")
        embed.add_field(name="Message Author", value=interaction.user.mention)

        # Extract relevant details from the Guild object
        guild_name = interaction.guild.name  # You can also use guild.id or other properties as needed
        embed.add_field(name="Server", value=guild_name)

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="get-message-id", description="Message-ID")
    @commands.has_any_role(1352254181305618495, 1352254181305618494)
    async def get_message_id(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("copy_message_id")
        
    @nextcord.slash_command(name="check-permissions", description="Überprüft die Berechtigungen des Bots.")
    @commands.has_any_role(1352254181305618495, 1352254181305618494)
    async def check_permissions(self, interaction: nextcord.Interaction):
        permissions = interaction.guild.me.guild_permissions  # Richtig eingerückt
        await interaction.response.send_message(f"Meine Berechtigungen:\n{permissions}", ephemeral=True)  # Auch richtig eingerückt

def setup(client):
    client.add_cog(CommandsCog(client))
    client.add_cog(ServerInfo(client))
