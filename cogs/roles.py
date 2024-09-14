import discord
from discord.ext import commands
from config import GUILD_ID

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready.")

    @commands.command(name='roles')
    async def roles(self, ctx):
        """Commande manuelle pour envoyer le message d'accueil et ajouter les réactions sur plusieurs messages."""
        guild = self.bot.get_guild(int(GUILD_ID))
        if guild is None:
            await ctx.send(f"Guild avec l'ID {int(GUILD_ID)} introuvable.")
            return

        channel = discord.utils.get(guild.text_channels, name='👋┊roles-et-filières')
        if channel is None:
            await ctx.send("Channel introuvable.")
            return

        try:
            # Premier message avec les premières réactions
            message1 = await channel.send(
                "Bienvenue sur le serveur de Montpellier Ynov Campus !\n\n"
                "Si tu n'as pas le role etudiant, commence par taper `!inscription"
                "Réagissez pour obtenir vos rôles (Partie 1):\n\n"
                "📱 pour B1 INFO\n📲 pour B2 INFO\n💻 pour B3 INFO\n🖥️ pour M1/M2 INFO\n\n"
                "📈 pour B1 MARCOM\n📉 pour B2 MARCOM\n📊 pour B3 MARCOM\n💶 pour M1/M2 MARCOM"
            )
            
            reactions1 = ['📱', '📲', '💻', '🖥️', '📈', '📉', '📊', '💶']
            for emoji in reactions1:
                await message1.add_reaction(emoji)

            # Deuxième message avec les réactions suivantes
            message2 = await channel.send(
                "Réagissez pour obtenir vos rôles (Partie 2):\n\n"
                "🏕️ pour B1 CREA\n🏜️ pour B2 CREA\n🎑 pour B3 CREA\n🏞️ pour M1/M2 CREA\n\n"
                "🎧 pour B1 AUDIO\n🎤 pour B2 AUDIO\n🎚️ pour B3 AUDIO"
            )

            reactions2 = ['🏕️', '🏜️', '🎑', '🏞️', '🎧', '🎤', '🎚️']
            for emoji in reactions2:
                await message2.add_reaction(emoji)

            # Troisième message avec les dernières réactions
            message3 = await channel.send(
                "Réagissez pour obtenir vos rôles (Partie 3):\n\n"
                "⛺ pour B1 ARCHI\n🏠 pour B2 ARCHI\n🏟️ pour B3 ARCHI\n🎢 pour M1/M2 ARCHI\n\n"
                "🗡️ pour B1 ANIM 3D\n⚔️ pour B2 ANIM 3D\n🔫 pour B3 ANIM 3D\n🎮 pour M1/M2 ANIM 3D\n\n"
                "👔 pour INTERVENANT(E)"
            )

            reactions3 = ['⛺', '🏠', '🏟️', '🎢', '🗡️', '⚔️', '🔫', '🎮', '👔']
            for emoji in reactions3:
                await message3.add_reaction(emoji)

        except Exception as e:
            await ctx.send(f"Erreur lors de l'envoi des messages: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id != GUILD_ID:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            print("Guild not found during reaction add.")
            return

        member = await guild.fetch_member(payload.user_id)
        etudiant_role = discord.utils.get(guild.roles, name="etudiant")
        if etudiant_role not in member.roles:
            return

        role_name = {
            '📱': "B1 INFO",
            '📲': "B2 INFO",
            '💻': "B3 INFO",
            '🖥️': "M1/M2 INFO",
            '📈': "B1 MARCOM",
            '📉': "B2 MARCOM",
            '📊': "B3 MARCOM",
            '💶': "M1/M2 MARCOM",
            '🏕️': "B1 CREA",
            '🏜️': "B2 CREA",
            '🎑': "B3 CREA",
            '🏞️': "M1/M2 CREA",
            '🎧': "B1 AUDIO",
            '🎤': "B2 AUDIO",
            '🎚️': "B3 AUDIO",
            '⛺': "B1 ARCHI",
            '🏠': "B2 ARCHI",
            '🏟️': "B3 ARCHI",
            '🎢': "M1/M2 ARCHI",
            '🗡️': "B1 3D ANIM",
            '⚔️': "B2 3D ANIM",
            '🔫': "B3 3D ANIM",
            '🎮': "M1/M2 3D ANIM",
            '👔': "INTERVENANT(E)"
        }.get(payload.emoji.name)

        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.add_roles(role)
                print(f"Added role {role_name} to {member.name}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id != GUILD_ID:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            print("Guild not found during reaction remove.")
            return

        member = await guild.fetch_member(payload.user_id)
        etudiant_role = discord.utils.get(guild.roles, name="etudiant")
        if etudiant_role not in member.roles:
            return

        role_name = {
            '📱': "B1 INFO",
            '📲': "B2 INFO",
            '💻': "B3 INFO",
            '🖥️': "M1/M2 INFO",
            '📈': "B1 MARCOM",
            '📉': "B2 MARCOM",
            '📊': "B3 MARCOM",
            '💶': "M1/M2 MARCOM",
            '🏕️': "B1 CREA",
            '🏜️': "B2 CREA",
            '🎑': "B3 CREA",
            '🏞️': "M1/M2 CREA",
            '🎧': "B1 AUDIO",
            '🎤': "B2 AUDIO",
            '🎚️': "B3 AUDIO",
            '⛺': "B1 ARCHI",
            '🏠': "B2 ARCHI",
            '🏟️': "B3 ARCHI",
            '🎢': "M1/M2 ARCHI",
            '🗡️': "B1 3D ANIM",
            '⚔️': "B2 3D ANIM",
            '🔫': "B3 3D ANIM",
            '🎮': "M1/M2 3D ANIM",
            '👔': "INTERVENANT(E)"
        }.get(payload.emoji.name)

        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.remove_roles(role)
                print(f"Removed role {role_name} from {member.name}")

async def setup(bot):
    print("Loading Roles Cog")
    await bot.add_cog(Roles(bot))
