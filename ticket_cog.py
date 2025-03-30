import nextcord
import config
from nextcord.ext import commands
import asyncio
import json
import os
from ticket_logs import save_ticket_logs


class TicketDropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Allgemeines-Support-Ticket", description="Erstelle ein allgemeines Support-Ticket."),
            nextcord.SelectOption(label="Bug-Report-Ticket", description="Erstelle ein Ticket für einen Bug-Report."),
            nextcord.SelectOption(label="Bewerbung", description="Erstelle ein Bewerbung-Ticket."),
        ]
        super().__init__(placeholder="Wähle die Art des Tickets aus...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        ticket_type = self.values[0]
        view = self.view
        if isinstance(view, TicketDropdownView):
            await view.create_ticket(interaction, ticket_type)


class TicketDropdownView(nextcord.ui.View):
    def __init__(self, guild, old_message=None):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())
        self.old_message = old_message
        self.guild = guild  # Guild-Instanz speichern

    async def create_ticket(self, interaction: nextcord.Interaction, ticket_type: str):
        role_1 = nextcord.utils.get(self.guild.roles, id=1352254181305618495)  # Owner
        role_2 = nextcord.utils.get(self.guild.roles, id=1352254181297094692)  # Admin
        role_3 = nextcord.utils.get(self.guild.roles, id=1352254181297094693)  # Mod team
        #undendlich erweiterbar

        if not all([role_1, role_2, role_3,]):
            return

        # Kategorien prüfen oder erstellen
        if ticket_type.lower() == "bewerbung":
            category_name = "Bewerbungen"
        else:
            category_name = "Tickets"

        category = nextcord.utils.get(interaction.guild.categories, name=category_name)
        if not category:
            category = await interaction.guild.create_category(name=category_name)

        # Berechtigungen für das Ticket
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
            interaction.user: nextcord.PermissionOverwrite(view_channel=True),
            role_1: nextcord.PermissionOverwrite(view_channel=True, send_messages=True),  # Owner
            role_2: nextcord.PermissionOverwrite(view_channel=True, send_messages=True),  # Admin
            role_3: nextcord.PermissionOverwrite(view_channel=True, send_messages=True),  # Mod Team
            #unendlich erweitrerbar
        }

        # Ticket-Channel erstellen
        channel_name = f"{interaction.user.name}-{ticket_type.lower()}-ticket"
        try:
            channel = await category.create_text_channel(name=channel_name, overwrites=overwrites)
        except Exception:
            return

        # Rückmeldung an den Benutzer
        try:
            await interaction.response.send_message(f"Dein {ticket_type}-Ticket wurde erstellt: {channel.mention}.", ephemeral=True)
        except Exception:
            return

        # Begrüßungsnachricht im Ticket-Channel
        embed = nextcord.Embed(
            title=f"Willkommen im {ticket_type} Support.",
            description="Das Team wurde informiert. Bitte teile uns dein Anliegen mit.",
            color=nextcord.Color.blue()
        )
        embed.set_footer(text="hehehehheh.")

        try:
            await channel.send(embed=embed, view=CloseButtons(channel))
        except Exception:
            return

        # Spezielle Nachricht für Bewerbungstickets
        if ticket_type.lower() == "bewerbung":
            try:
                link_embed = nextcord.Embed(
                    title="Bewerbungsformular",
                    description="[Klicke hier, um das Bewerbungsformular auszufüllen](nein)",
                    color=nextcord.Color.green(),
                )
                await channel.send(embed=link_embed)
            except Exception:
                return


class CloseButtons(nextcord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=None)
        self.channel = channel

    @nextcord.ui.button(label="Ticket schließen", style=nextcord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Ticket-Logs speichern
        try:
            await save_ticket_logs(self.channel)
        except Exception:
            pass

        embed = nextcord.Embed(
            title="Ticket Schließen",
            description="Das Ticket wird in wenigen Sekunden geschlossen.",
            color=nextcord.Color.red(),
        )
        try:
            await interaction.response.send_message(embed=embed, ephemeral=False)
            await asyncio.sleep(2)
            await self.channel.delete()
        except Exception:
            pass


class TicketBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        channel_id = 1321064896384729190  # Ticket-Channel ID anpassen
        channel = self.client.get_channel(channel_id)

        if channel:
            message_id_path = "ticket_logs/ticket_message_id.json"

            # Prüfen, ob die Datei existiert und korrekt ist
            if os.path.exists(message_id_path):
                try:
                    with open(message_id_path, "r") as file:
                        data = json.load(file)
                        message_id = data.get("message_id")

                    if message_id:
                        # Bestehende Nachricht bearbeiten
                        old_message = await channel.fetch_message(message_id)
                        embed = nextcord.Embed(
                            title="Meta.Games suppe",
                            description="Bitte wähle den Typ des Tickets aus, das du erstellen möchtest.",
                            color=nextcord.Color.blue(),
                        )
                        guild = channel.guild  # Hole die Guild-Instanz
                        await old_message.edit(embed=embed, view=TicketDropdownView(guild, old_message))
                        return
                except (json.JSONDecodeError, KeyError, nextcord.NotFound):
                    pass

            # Wenn keine gültige Nachricht existiert, eine neue senden
            embed = nextcord.Embed(
                title="Meta.Games suppe",
                description="Bitte wähle den Typ des Tickets aus, das du erstellen möchtest.",
                color=nextcord.Color.blue(),
            )
            message = await channel.send(embed=embed, view=TicketDropdownView(channel.guild, None))

            # Nachricht-ID speichern
            with open(message_id_path, "w") as file:
                json.dump({"message_id": message.id}, file)

def setup(client):
    client.add_cog(TicketBot(client))