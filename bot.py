import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))  # Assure-toi que cette variable est définie dans .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Charger les cogs
for cog in os.listdir('cogs'):
    if cog.endswith('.py') and cog != '__init__.py':
        bot.load_extension(f'cogs.{cog[:-3]}')

@bot.event
async def on_ready():
    print(f'{bot.user.name} est connecté au serveur.')

bot.run(TOKEN)
