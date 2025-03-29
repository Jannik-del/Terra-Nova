import nextcord
from nextcord.ext import commands
from nextcord import interactions, application_command
import config
import asyncio
import traceback
#import openai
from ticket_logs import save_ticket_logs



client = commands.Bot(command_prefix="/", intents=nextcord.Intents.all())
client.load_extension("command_list")
client.load_extension("User-infos_cog")
client.load_extension("welcome-cog")
client.load_extension("ticket_cog")
client.load_extension("moderation_cog")
client.load_extension("debug")
client.load_extension("admin-messages")
client.load_extension("Message_menu_config")
client.load_extension("temp-voice")
client.load_extension("voice_player")
client.load_extension("Leave")
client.load_extension("rules")
client.load_extension("reload")




class selfroles(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)
        self.value = None
        guild = client.get_guild(config.GUILD_ID)

        # buttons
        community = nextcord.ui.Button(label="Community", style=nextcord.ButtonStyle.blurple, emoji="👥", row=0)
        ingupdate = nextcord.ui.Button(label="ing-updates", style=nextcord.ButtonStyle.blurple, emoji="🎮", row=0)
        werbung = nextcord.ui.Button(label="werbung", style=nextcord.ButtonStyle.blurple, emoji="📲", row=1)
        giveaway = nextcord.ui.Button(label="Giveaway", style=nextcord.ButtonStyle.blurple, emoji="🎉", row=1)
        technik = nextcord.ui.Button(label="Technik / Entwicklung", style=nextcord.ButtonStyle.blurple, emoji="☎️", row=2)

        # roles
        community_role = nextcord.utils.get(guild.roles, id=1324365735413415957)
        gaming_role = nextcord.utils.get(guild.roles, id=1324365901126176791)#NEU
        werbung_role = nextcord.utils.get(guild.roles, id=1324365982113861652)#NEU
        giveaway_role = nextcord.utils.get(guild.roles, id=1324366077173698600)#NEU
        technik_role = nextcord.utils.get(guild.roles, id=1324366164905955442)#NEU

        # adding items to view
        self.add_item(community)
        self.add_item(ingupdate)
        self.add_item(werbung)
        self.add_item(giveaway)
        self.add_item(technik)

        # callbacks on buttons
        async def community_callback(interaction: nextcord.Interaction):
            role = community_role
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f":white_check_mark: - {role.mention} wurde erfolgreich "
                                                        f"entfernt.", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                    await asyncio.sleep(1)
                    await interaction.response.send_message(f":white_check_mark: - Du hast {role.mention} erfolgreich "
                                                            f"erhalten.", ephemeral=True)
                except:
                    await interaction.response.send_message(f":x: - Etwas ist schief geleufen. Bitte wende dich in "
                                                            f"<#1321064896384729190> an den Support.", ephemeral=True)
                    traceback.print_exc()

        async def ingupdate_callback(interaction: nextcord.Interaction):
            role = gaming_role
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f":white_check_mark: - {role.mention} wurde erfolgreich "
                                                        f"entfernt.", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                    await asyncio.sleep(1)
                    await interaction.response.send_message(
                        f":white_check_mark: - Du hast {role.mention} erfolgreich "
                        f"erhalten.", ephemeral=True)
                except:
                    await interaction.response.send_message(f":x: - Etwas ist schief geleufen. Bitte wende dich in "
                                                            f"<#1321064896384729190> an den Support.",
                                                            ephemeral=True)
                    traceback.print_exc()


        async def werbung_callback(interaction: nextcord.Interaction):
            role = werbung_role
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f":white_check_mark: - {role.mention} wurde erfolgreich "
                                                        f"entfernt.", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                    await asyncio.sleep(1)
                    await interaction.response.send_message(
                        f":white_check_mark: - Du hast {role.mention} erfolgreich "
                        f"erhalten.", ephemeral=True)
                except:
                    await interaction.response.send_message(f":x: - Etwas ist schief geleufen. Bitte wende dich in "
                                                            f"<#1321064896384729190> an den Support.",
                                                            ephemeral=True)
                    traceback.print_exc()


        async def giveaway_callback(interaction: nextcord.Interaction):
            role = giveaway_role
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f":white_check_mark: - {role.mention} wurde erfolgreich "
                                                        f"entfernt.", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                    await asyncio.sleep(1)
                    await interaction.response.send_message(
                        f":white_check_mark: - Du hast {role.mention} erfolgreich "
                        f"erhalten.", ephemeral=True)
                except:
                    await interaction.response.send_message(f":x: - Etwas ist schief geleufen. Bitte wende dich in "
                                                            f"<#1321064896384729190> an den Support.",
                                                            ephemeral=True)
                    traceback.print_exc()

        async def techik_callback(interaction: nextcord.Interaction):
            role = technik_role
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f":white_check_mark: - {role.mention} wurde erfolgreich "
                                                        f"entfernt.", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                    await asyncio.sleep(1)
                    await interaction.response.send_message(
                        f":white_check_mark: - Du hast {role.mention} erfolgreich "
                        f"erhalten.", ephemeral=True)
                except:
                    await interaction.response.send_message(f":x: - Etwas ist schief geleufen. Bitte wende dich in "
                                                            f"<#1321064896384729190> an den Support.",
                                                            ephemeral=True)
                    traceback.print_exc()
        community.callback = community_callback
        ingupdate.callback = ingupdate_callback
        werbung.callback = werbung_callback
        technik.callback = techik_callback
        giveaway.callback = giveaway_callback


@client.event
async def on_ready():
    await client.sync_all_application_commands()
    print(f'Bot ist bereit als {client.user}')#

    selfroles_channel = client.get_channel(config.SELFROLES_CHANNEL_ID)

    selfroles_embed = nextcord.Embed(
        title="Wähle deine Rollen",
        description=(  # Beschreibung bleibt unverändert...
            ":light_blue_heart: **Community**: 👥 Erhalte Pings für fast alles.\n\n"
            ":red_circle: **ingupdate**: 🎮 Erhalte Pings, wenn jemand Mitspieler sucht und @Gaming verwendet.\n\n"
            ":grey_heart: **Werbung**: 📲 Du erhältst immer Pings, wenn etwas Neues oder eine Zusammenarbeit angekündigt wird.\n\n"
            ":green_circle: **Giveaway**: 🎉 Du wirst gepingt, wenn ein Giveaway stattfindet.\n\n"
            ":blue_circle: **Technik & Entwicklung**: 📡 Erhalte Pings, wenn wir bei der Entwicklung Fortschritte machen."
        )
    )

    selfroles_message = await selfroles_channel.fetch_message(config.SELFROLES_MESSAGE_ID)

    # Check if the channel is None
    if selfroles_channel is None:
        print(f"Error: Channel with ID {config.SELFROLES_CHANNEL_ID} could not be found.")
    else:
        try:
            selfroles_message = await selfroles_channel.fetch_message(config.SELFROLES_MESSAGE_ID)
            print(f"Message fetched: {selfroles_message.content}")
        except Exception as e:
            print(f"Error fetching the message: {e}")

    await selfroles_message.edit(embed=selfroles_embed, view=selfroles())

    activity = nextcord.Activity(
        type=nextcord.ActivityType.playing,  # Aktivitätsart
        name="Meta.Games",  # Aktivitätsname
        state="Meta.Games chat & support",  # Status-Nachricht
        details="watching u",  # Aktivitätsdetails
        assets={"large_image": "", "large_text": "Manage"}  # Bild-Assets
    )

    await client.change_presence(activity=activity)

client.run(config.TOKEN)


#@bot.slash_command(name="ping", description="Ping Pong")
#async def ping(interaction: discord.Interaction):
     #await interaction.response.send_message("pong")