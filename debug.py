import nextcord
from nextcord.ext import commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="ping", description="Get the bot's latency")
    @commands.has_any_role(1352254181305618495, 1352254181297094695, 1352254181297094692)
    async def ping(self, interaction: nextcord.Interaction):
        # Berechne die Latenz in Millisekunden
        latency = self.client.latency * 1000  # in ms umrechnen
        await interaction.response.send_message(f'Pong! Latenz: {latency:.2f}ms')

# Setup-Funktion, um den Cog zum Bot hinzuzufügen
def setup(client):
    client.add_cog(Ping(client))