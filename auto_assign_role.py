import nextcord
from nextcord.ext import commands

class AutoAssignRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = member.guild.get_role(1352254181280583718)  # Ersetze die ID durch die tatsächliche Rollen-ID

        if role is not None:
            # Zuweisung der Rolle zum neuen Mitglied
            await member.add_roles(role)
            print(f"Automatische Rolle '{role.name}' wurde an {member.name} vergeben.")
        else:
            print(f"Rolle 'Member' konnte nicht gefunden werden.")

def setup(client):
    client.add_cog(AutoAssignRole(client))