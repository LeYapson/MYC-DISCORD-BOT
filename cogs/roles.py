import discord
from discord.ext import commands
from config import GUILD_ID

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(GUILD_ID)
        channel = discord.utils.get(guild.text_channels, name='👋┊roles-et-filières')

        if channel:
            message = await channel.send(
                "Bienvenue sur le serveur de Ynov Campus !\n\n"
                "Vous devez d'abord confirmer votre appartenance à l'école en utilisant la commande `!inscription <email>`.\n\n"
                "Une fois inscrit, vous pouvez choisir votre filière en réagissant à ce message.\n\n"
                "Réagissez pour obtenir vos rôles:\n"
                "📱 pour B1 INFO\n💻 pour B2 INFO\n🖥️ pour B3 INFO\n🖥️ pour M1/M2 INFO\n\n"
                "📈 pour B1 MARCOM\n📉 pour B2 MARCOM\n📊 pour B3 MARCOM\n📊 pour M1/M2 MARCOM\n\n"
                "🏕️ pour B1 CREA\n🏜️ pour B2 CREA\n🏞️ pour B3 CREA\n🏞️ pour M1/M2 CREA\n\n"
                "🎧 pour B1 AUDIO\n🎤 pour B2 AUDIO\n🎚️ pour B3 AUDIO\n🎚️ pour M1/M2 AUDIO\n\n"
                "⛺ pour B1 ARCHI\n🏠 pour B2 ARCHI\n🏟️ pour B3 ARCHI\n🏟️ pour M1/M2 ARCHI\n\n"
                "🗡️ pour B1 ANIM 3D\n⚔️ pour B2 ANIM 3D\n🔫 pour B3 ANIM 3D\n🔫 pour M1/M2 ANIM 3D\n\n"
                "👔 pour INTERVENANT(E)"
            )

            reactions = ['📱', '💻', '🖥️', '📈', '📉', '📊', '🏕️', '🏜️', '🏞️', '🎧', '🎤', '🎚️', '⛺', '🏠', '🏟️', '🗡️', '⚔️', '🔫', '👔']
            for emoji in reactions:
                await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id != GUILD_ID:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)

        etudiant_role = discord.utils.get(guild.roles, name="etudiant")
        if etudiant_role not in member.roles:
            return

        role_name = {
            '📱': "B1 INFO",
            '💻': "B2 INFO",
            '🖥️': "B3 INFO",
            '📈': "B1 MARCOM",
            '📉': "B2 MARCOM",
            '📊': "B3 MARCOM",
            '🏕️': "B1 CREA",
            '🏜️': "B2 CREA",
            '🏞️': "B3 CREA",
            '🎧': "B1 AUDIO",
            '🎤': "B2 AUDIO",
            '🎚️': "B3 AUDIO",
            '⛺': "B1 ARCHI",
            '🏠': "B2 ARCHI",
            '🏟️': "B3 ARCHI",
            '🗡️': "B1 ANIM 3D",
            '⚔️': "B2 ANIM 3D",
            '🔫': "B3 ANIM 3D",
            '👔': "INTERVENANT(E)"
        }.get(payload.emoji.name)

        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id != GUILD_ID:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)

        etudiant_role = discord.utils.get(guild.roles, name="etudiant")
        if etudiant_role not in member.roles:
            return

        role_name = {
            '📱': "B1 INFO",
            '💻': "B2 INFO",
            '🖥️': "B3 INFO",
            '📈': "B1 MARCOM",
            '📉': "B2 MARCOM",
            '📊': "B3 MARCOM",
            '🏕️': "B1 CREA",
            '🏜️': "B2 CREA",
            '🏞️': "B3 CREA",
            '🎧': "B1 AUDIO",
            '🎤': "B2 AUDIO",
            '🎚️': "B3 AUDIO",
            '⛺': "B1 ARCHI",
            '🏠': "B2 ARCHI",
            '🏟️': "B3 ARCHI",
            '🗡️': "B1 ANIM 3D",
            '⚔️': "B2 ANIM 3D",
            '🔫': "B3 ANIM 3D",
            '👔': "INTERVENANT(E)"
        }.get(payload.emoji.name)

        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.remove_roles(role)

def setup(bot):
    bot.add_cog(Roles(bot))
