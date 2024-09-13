import discord
from discord.ext import commands
from config import GUILD_ID

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='test')
    async def test_command(self, ctx):
        await ctx.send("Command test works!")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready. Setting up roles message...")
        guild = self.bot.get_guild(int(GUILD_ID))
        if guild is None:
            print(f"Guild with ID {int(GUILD_ID)} not found.")
            return

        channel = discord.utils.get(guild.text_channels, name='👋┊roles-et-filières')
        if channel is None:
            print("Channel not found.")
            return

        try:
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
            print("Message sent. Adding reactions...")
            
            reactions = ['📱', '💻', '🖥️', '📈', '📉', '📊', '🏕️', '🏜️', '🏞️', '🎧', '🎤', '🎚️', '⛺', '🏠', '🏟️', '🗡️', '⚔️', '🔫', '👔']
            for emoji in reactions:
                try:
                    await message.add_reaction(emoji)
                    print(f"Added reaction: {emoji}")
                except Exception as e:
                    print(f"Error adding reaction {emoji}: {e}")

        except Exception as e:
            print(f"Error setting up roles message: {e}")

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
                print(f"Removed role {role_name} from {member.name}")

async def setup(bot):
    print("Loading Roles Cog")
    await bot.add_cog(Roles(bot))
