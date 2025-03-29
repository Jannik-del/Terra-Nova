import nextcord
from nextcord.ext import commands
from nextcord import SelectOption, Interaction

class MessageConfigMenu(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="message_menu_für_config")
    @commands.has_any_role(1352254181305618495)  # Beispiel Roll-IDs
    async def config_message_menu(self, ctx):
        # Erstellung des Dropdown-Menüs für die Kanalauswahl
        channel_options = [
            SelectOption(label="Self_roles_message", value="1352254181880107135"),
            SelectOption(label="Welcome_message", value="1352254181741957123"),
            SelectOption(label="Support_message", value="1352254182014582798"),
            SelectOption(label="--", value="--"),
        ]

        channel_select = nextcord.ui.Select(
            placeholder="Wähle einen Kanal",
            options=channel_options
        )

        # Menü für das Nachrichtenformat
        format_options = [
            SelectOption(label="Text", value="text"),
            SelectOption(label="Embed", value="embed"),
            SelectOption(label="Codeblock", value="codeblock")
        ]

        format_select = nextcord.ui.Select(
            placeholder="Wähle das Nachrichtenformat",
            options=format_options
        )

        # Erstellung einer View mit interaktiven Komponenten
        class MessageConfigView(nextcord.ui.View):
            def __init__(self, client):
                super().__init__()
                self.client = client  # Speichere den Client
                self.channel_select = channel_select
                self.format_select = format_select
                self.add_item(self.channel_select)
                self.add_item(self.format_select)

            @nextcord.ui.button(label="Nachricht verfassen", style=nextcord.ButtonStyle.primary)
            async def write_message_button(self, button: nextcord.ui.Button, interaction: Interaction):
                # Öffne ein Modal zur Texteingabe
                modal = MessageModal(
                    channel_id=int(self.channel_select.values[0]),
                    message_format=self.format_select.values[0],
                    client=self.client
                )
                await interaction.response.send_modal(modal)

        # Modal zur Eingabe von Titel und Nachrichtentext
        class MessageModal(nextcord.ui.Modal):
            def __init__(self, channel_id, message_format, client):
                self.channel_id = channel_id
                self.message_format = message_format
                self.client = client

                super().__init__(title="Nachricht verfassen")
                
                # Eingabefeld für den Titel
                self.title_input = nextcord.ui.TextInput(
                    label="Titel (nur für Embeds)",
                    placeholder="Gib hier den Titel ein...",
                    style=nextcord.TextInputStyle.short,
                    required=False
                )
                self.add_item(self.title_input)
                
                # Eingabefeld für den Inhalt
                self.message_input = nextcord.ui.TextInput(
                    label="Nachricht",
                    placeholder="Gib hier deine Nachricht ein...",
                    style=nextcord.TextInputStyle.paragraph,
                    required=True
                )
                self.add_item(self.message_input)

            async def callback(self, interaction: Interaction):
                channel = self.client.get_channel(self.channel_id)
                if not channel:
                    await interaction.response.send_message("Channel konnte nicht gefunden werden.", ephemeral=True)
                    return

                # Nachricht senden basierend auf dem ausgewählten Format
                if self.message_format == "text":
                    await channel.send(self.message_input.value)
                elif self.message_format == "embed":
                    embed = nextcord.Embed(
                        title=self.title_input.value if self.title_input.value else "Admin Nachricht",
                        description=self.message_input.value,
                        color=nextcord.Color.blue()
                    )
                    await channel.send(embed=embed)
                elif self.message_format == "codeblock":
                    codeblock_message = f"```\n{self.message_input.value}\n```"
                    await channel.send(codeblock_message)

                await interaction.response.send_message(
                    f"Nachricht erfolgreich im Kanal {channel.name} gesendet.", ephemeral=True
                )

        view = MessageConfigView(client=self.client)
        await ctx.send("Wähle den Kanal und das Nachrichtenformat aus:", view=view)

def setup(client):
    client.add_cog(MessageConfigMenu(client))
