import nextcord
from nextcord.ext import commands

class Regeln(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="rules")
    @commands.has_any_role(1352254181305618495)
    async def regeln(self, ctx):
        embed = nextcord.Embed(
            title="📜 Terra Nova Server Regeln",
            description="Bitte halte dich an die folgenden Regeln, um eine angenehme Community zu gewährleisten.",
            color=nextcord.Color.red(),
            timestamp=nextcord.utils.utcnow()
        )

        # Verhaltensregeln
        embed.add_field(
            name="**1️⃣ Verhaltensregeln (Teil 1):**",
            value=(
                "**1.1:** Keine Spam-Nachrichten oder unangemessenen Inhalte erstellen oder teilen.\n"
                "**1.2:** Wir sind nicht für private Streitigkeiten zuständig. Klärung über Support ist nicht erlaubt.\n"
                "**1.3:** Zweitaccounts sind den verboten wenn man die zum umgehen eienr bestrafung nutzt.\n"
            ),
            inline=False
        )

        embed.add_field(
            name="**1️⃣ Verhaltensregeln (Teil 2):**",
            value=(
                "**1.4:** Wähle einen angemessenen und nicht beleidigenden Server-Nickname.\n"
                "**1.5:** NSFW-Inhalte sind verboten und führen zu Konsequenzen.\n"
                "**1.6:** Unangemessene Avatare oder Profilbilder sind nicht erlaubt und führen zu einem permanenten Ban (außer nach absprache)."
            ),
            inline=False
        )

        # Verwendung von Sprache
        embed.add_field(
            name="**2️⃣ Verwendung von Sprache:**",
            value=(
                "**2.1:** Spammen von Emojis wird bestraft.\n"
                "**2.2:** Keine Beleidigungen oder unerwünschte Wörter.\n"
                "**2.3:** Keine Bedrohungen oder Beleidigungen gegen andere Benutzer.\n"
                "**2.4:** Rassistische, sexistische oder diskriminierende Äußerungen sind verboten.\n"
                "**2.5:** Übermäßiger Gebrauch von Großbuchstaben (Capslock) ist nicht erlaubt.\n"
                "**2.6:** Diese Regeln gelten auch in Voice-Channels."
            ),
            inline=False
        )

        # Datenschutz
        embed.add_field(
            name="**3️⃣ Datenschutz:**",
            value=(
                "**3.1:** Keine Weitergabe persönlicher Informationen anderer Nutzer ohne Zustimmung.\n"
                "**3.2:** Teile keine Nachrichten, die gegen Datenschutzgesetze verstoßen.\n"
                "**3.3:** Aufzeichnungen von Gesprächen ohne Zustimmung sind verboten und führen zu einem permanenten Bann (außer man hat einen guten grund dafür denn wird es weiter geklärt)."
            ),
            inline=False
        )

        # Inhalte der Nachrichten
        embed.add_field(
            name="**4️⃣ Inhalte der Nachrichten:**",
            value=(
                "**4.1:** Keine illegalen Inhalte oder Falschinformationen.\n"
                "**4.2:** Politische, religiöse oder sexuelle Themen sind nicht erwünscht.\n"
                "**4.3:** Fremdwerbung ist verboten. Öffne ein Ticket bei Verstößen."
            ),
            inline=False
        )

        # Verhalten gegenüber Teammitgliedern
        embed.add_field(
            name="**5️⃣ Verhalten gegenüber Teammitgliedern (Teil 1):**",
            value=(
                "**5.1:** Moderatoren müssen ihre Handlungen nicht rechtfertigen. Häufiges Nachfragen kann Strafen verlängern.\n"
                "**5.2:** Missbrauch des Supports durch Falschmeldungen oder Belästigungen ist verboten.\n"
                "**5.3:** Kontaktaufnahme mit Teammitgliedern per DM ist nur im Notfall erlaubt.\n"
                "**5.4:** Unnötiges Pingen von Teammitgliedern ist verboten und wird bestraft."
            ),
            inline=False
        )

        # Support
        embed.add_field(
            name="**6️⃣ Support:**",
            value=(
                "**6.1:** Support erfolgt ausschließlich über Tickets.\n"
                "**6.2:** Entscheidungen des Teams sind zu respektieren."
            ),
            inline=False
        )

        # Weiteres
        embed.add_field(
            name="**7️⃣ Weiteres:**",
            value=(
                "**7.1:** Das Team hat das letzte Wort, unabhängig vom Regelwerk.\n"
                "**7.2:** Das Team hat Hausrecht und kann bei Bedarf ohne Angabe von Gründen handeln."
            ),
            inline=False
        )

        embed.set_footer(text="Diese Regeln können ohne Ankündigung geändert werden.")
        embed.add_field(
            name="**Links:**",
            value=" <#1352254181741957125> | [Discord TOS](https://discord.com/terms)",
            inline=False
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Regeln(bot))
