import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

TOKEN = os.getenv('DISCORD-TOKEN')
if TOKEN is None:
    raise ValueError("Le token Discord n'est pas défini dans les variables d'environnement.")
GUILD_ID = 1004015076002504715  # Assure-toi que cette variable est définie dans .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} est connecté au serveur.')

    # Charger les extensions (cogs)
    for cog in os.listdir('./cogs'):
        if cog.endswith('.py') and cog != '__init__.py':  # Exclure __init__.py
            try:
                await bot.load_extension(f'cogs.{cog[:-3]}')
                print(f'Extension {cog} chargée.')
            except Exception as e:
                print(f'Erreur lors du chargement de l\'extension {cog}: {e}')

bot.run(TOKEN)
