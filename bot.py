# bot.py
import discord
from discord.ext import commands
import smtplib
import random
import re
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD-TOKEN')
GUILD_ID = 1004015076002504715  # Remplacer par l'ID de votre serveur
EMAIL_DOMAIN = '@ynov.com'
VERIFICATION_CODES = {}  # Stocker les codes de vérification ici

# Configurer le bot
intents = discord.Intents.default()
intents.messages = True  # Pour lire le contenu des messages
intents.message_content = True  # Intention pour le contenu des messages
intents.members = True  # Si vous devez interagir avec les membres du serveur

bot = commands.Bot(command_prefix='!', intents=intents)

# Fonction pour envoyer un e-mail avec un code de vérification
def send_verification_email(email_address, verification_code):
    sender_email = os.getenv('SENDER-EMAIL')
    password = os.getenv('SENDER-PASSWORD')
    message = f"""\
Subject: Code de verification

Votre code de verification est : {verification_code}
"""

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, email_address, message)
        server.quit()
        print(f"Code envoyé à {email_address}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

# Commande pour débuter l'inscription
@bot.command(name='inscription')
async def inscription(ctx, email: str):
    # Vérifier si l'utilisateur a déjà le rôle "Étudiant"
    role = discord.utils.get(ctx.guild.roles, name="etudiant")
    if role in ctx.author.roles:
        await ctx.send("Vous avez déjà le rôle Étudiant, l'inscription est terminée.")
        return
    
    # Vérifier que l'e-mail appartient à l'institution
    if not re.match(rf'^[\w\.-]+{EMAIL_DOMAIN}$', email):
        await ctx.send(f"Veuillez entrer une adresse e-mail valide se terminant par {EMAIL_DOMAIN}.")
        return

    # Générer et stocker un code de vérification
    verification_code = random.randint(100000, 999999)
    VERIFICATION_CODES[ctx.author.id] = (email, verification_code)

    # Envoyer le code à l'adresse e-mail
    send_verification_email(email, verification_code)
    await ctx.send(f"Un code de vérification a été envoyé à {email}. Veuillez l'entrer avec la commande `!verifier <code>`.")

# Commande pour vérifier le code
@bot.command(name='verifier')
async def verifier(ctx, code: int):
    if ctx.author.id not in VERIFICATION_CODES:
        await ctx.send("Vous n'avez pas encore initié le processus d'inscription.")
        return

    email, correct_code = VERIFICATION_CODES[ctx.author.id]

    if code == correct_code:
        # Ajouter un rôle après la vérification (le rôle "Étudiant")
        role = discord.utils.get(ctx.guild.roles, name="etudiant")
        await ctx.author.add_roles(role)
        await ctx.send("Votre compte a été vérifié et vous avez reçu le rôle Étudiant.")
        del VERIFICATION_CODES[ctx.author.id]
    else:
        await ctx.send("Le code est incorrect. Veuillez réessayer.")

@bot.command(name='clear')
@commands.has_permissions(administrator=True)  # Restrict command to users with Admin permissions
async def clear(ctx, amount: int):
    if amount < 1:
        await ctx.send("You need to specify a positive number of messages to delete.")
        return
    elif amount > 100:  # Discord's maximum limit for bulk delete
        await ctx.send("You cannot delete more than 100 messages at a time.")
        return
    
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {len(deleted)} messages.", delete_after=5)  # Message disappears after 5 seconds

# Ajouter les rôles par réaction
@bot.event
async def on_ready():
    print(f'{bot.user.name} est connecté au serveur.')

    # Envoyer un message de bienvenue avec les réactions pour choisir les rôles
    print(GUILD_ID)
    guild = bot.get_guild(int(GUILD_ID))
    channel = discord.utils.get(guild.text_channels, name='👋┊roles-et-filières')  # Changez le nom du canal si besoin

    if channel is not None:
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

        # Ajout des réactions au message
        reactions = ['📱', '💻', '🖥️', '📈', '📉', '📊', '🏕️', '🏜️', '🏞️', '🎧', '🎤', '🎚️', '⛺', '🏠', '🏟️', '🗡️', '⚔️', '🔫', '👔']
        for emoji in reactions:
            await message.add_reaction(emoji)


# Attribuer le rôle en fonction de la réaction
@bot.event
async def on_raw_reaction_add(payload):
    if payload.guild_id != GUILD_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)  # Fetch the member if not cached

    # Check if the user has the "Étudiant" role
    etudiant_role = discord.utils.get(guild.roles, name="etudiant")
    if etudiant_role not in member.roles:
        print(f"{member} does not have the 'Étudiant' role.")
        return  # Exit if the user doesn't have the "Étudiant" role

    # Assign roles based on the reaction
    role = None

    if payload.emoji.name == '📱':
        role = discord.utils.get(guild.roles, name="B1 INFO")
    elif payload.emoji.name == '💻':
        role = discord.utils.get(guild.roles, name="B2 INFO")
    elif payload.emoji.name == '🖥️':
        role = discord.utils.get(guild.roles, name="B3 INFO")
    elif payload.emoji.name == '📈':
        role = discord.utils.get(guild.roles, name="B1 MARCOM")
    elif payload.emoji.name == '📉':
        role = discord.utils.get(guild.roles, name="B2 MARCOM")
    elif payload.emoji.name == '📊':
        role = discord.utils.get(guild.roles, name="B3 MARCOM")
    elif payload.emoji.name == '🏕️':
        role = discord.utils.get(guild.roles, name="B1 CREA")
    elif payload.emoji.name == '🏜️':
        role = discord.utils.get(guild.roles, name="B2 CREA")
    elif payload.emoji.name == '🏞️':
        role = discord.utils.get(guild.roles, name="B3 CREA")
    elif payload.emoji.name == '🎧':
        role = discord.utils.get(guild.roles, name="B1 AUDIO")
    elif payload.emoji.name == '🎤':
        role = discord.utils.get(guild.roles, name="B2 AUDIO")
    elif payload.emoji.name == '🎚️':
        role = discord.utils.get(guild.roles, name="B3 AUDIO")
    elif payload.emoji.name == '⛺':
        role = discord.utils.get(guild.roles, name="B1 ARCHI")
    elif payload.emoji.name == '🏠':
        role = discord.utils.get(guild.roles, name="B2 ARCHI")
    elif payload.emoji.name == '🏟️':
        role = discord.utils.get(guild.roles, name="B3 ARCHI")
    elif payload.emoji.name == '🗡️':
        role = discord.utils.get(guild.roles, name="B1 ANIM 3D")
    elif payload.emoji.name == '⚔️':
        role = discord.utils.get(guild.roles, name="B2 ANIM 3D")
    elif payload.emoji.name == '🔫':
        role = discord.utils.get(guild.roles, name="B3 ANIM 3D")
    elif payload.emoji.name == '👔':
        role = discord.utils.get(guild.roles, name="INTERVENANT(E)")

    if role:
        await member.add_roles(role)


# Retirer le rôle si la réaction est supprimée
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.guild_id != GUILD_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)  # Fetch the member if not cached

    # Check if the user has the "Étudiant" role
    etudiant_role = discord.utils.get(guild.roles, name="etudiant")
    if etudiant_role not in member.roles:
        print(f"{member} does not have the 'Étudiant' role.")
        return  # Exit if the user doesn't have the "Étudiant" role

    # Remove roles based on the reaction
    role = None

    if payload.emoji.name == '📱':
        role = discord.utils.get(guild.roles, name="B1 INFO")
    elif payload.emoji.name == '💻':
        role = discord.utils.get(guild.roles, name="B2 INFO")
    elif payload.emoji.name == '🖥️':
        role = discord.utils.get(guild.roles, name="B3 INFO")
    elif payload.emoji.name == '📈':
        role = discord.utils.get(guild.roles, name="B1 MARCOM")
    elif payload.emoji.name == '📉':
        role = discord.utils.get(guild.roles, name="B2 MARCOM")
    elif payload.emoji.name == '📊':
        role = discord.utils.get(guild.roles, name="B3 MARCOM")
    elif payload.emoji.name == '🏕️':
        role = discord.utils.get(guild.roles, name="B1 CREA")
    elif payload.emoji.name == '🏜️':
        role = discord.utils.get(guild.roles, name="B2 CREA")
    elif payload.emoji.name == '🏞️':
        role = discord.utils.get(guild.roles, name="B3 CREA")
    elif payload.emoji.name == '🎧':
        role = discord.utils.get(guild.roles, name="B1 AUDIO")
    elif payload.emoji.name == '🎤':
        role = discord.utils.get(guild.roles, name="B2 AUDIO")
    elif payload.emoji.name == '🎚️':
        role = discord.utils.get(guild.roles, name="B3 AUDIO")
    elif payload.emoji.name == '⛺':
        role = discord.utils.get(guild.roles, name="B1 ARCHI")
    elif payload.emoji.name == '🏠':
        role = discord.utils.get(guild.roles, name="B2 ARCHI")
    elif payload.emoji.name == '🏟️':
        role = discord.utils.get(guild.roles, name="B3 ARCHI")
    elif payload.emoji.name == '🗡️':
        role = discord.utils.get(guild.roles, name="B1 ANIM 3D")
    elif payload.emoji.name == '⚔️':
        role = discord.utils.get(guild.roles, name="B2 ANIM 3D")
    elif payload.emoji.name == '🔫':
        role = discord.utils.get(guild.roles, name="B3 ANIM 3D")
    elif payload.emoji.name == '👔':
        role = discord.utils.get(guild.roles, name="INTERVENANT(E)")

    if role:
        await member.remove_roles(role)

async def add_reaction_with_rate_limit(message, emoji):
    try:
        await message.add_reaction(emoji)
    except discord.HTTPException as e:
        if e.code == 429:  # Rate limited
            retry_after = e.retry_after
            print(f"Rate limited. Retrying after {retry_after} seconds.")
            await asyncio.sleep(retry_after)
            await add_reaction_with_rate_limit(message, emoji)

# Lancer le bot
bot.run(TOKEN)
