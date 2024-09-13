import discord
from discord.ext import commands
import smtplib
import random
import re
import os
from config import EMAIL_DOMAIN

VERIFICATION_CODES = {}

def send_verification_email(email_address, verification_code):
    sender_email = os.getenv('SENDER-EMAIL')
    password = os.getenv('SENDER-PASSWORD')
    message = f"""\
Subject: Code de vérification

Votre code de vérification est : {verification_code}
"""

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, email_address, message)
        server.quit()
        print(f"Code envoyé à {email_address}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='inscription')
    async def inscription(self, ctx, email: str):
        role = discord.utils.get(ctx.guild.roles, name="etudiant")
        if role in ctx.author.roles:
            await ctx.send("Vous avez déjà le rôle Étudiant, l'inscription est terminée.")
            return

        if not re.match(rf'^[\w\.-]+{EMAIL_DOMAIN}$', email):
            await ctx.send(f"Veuillez entrer une adresse e-mail valide se terminant par {EMAIL_DOMAIN}.")
            return

        verification_code = random.randint(100000, 999999)
        VERIFICATION_CODES[ctx.author.id] = (email, verification_code)
        send_verification_email(email, verification_code)
        await ctx.send(f"Un code de vérification a été envoyé à {email}. Veuillez l'entrer avec la commande `!verifier <code>`.")

    @commands.command(name='verifier')
    async def verifier(self, ctx, code: int):
        if ctx.author.id not in VERIFICATION_CODES:
            await ctx.send("Vous n'avez pas encore initié le processus d'inscription.")
            return

        email, correct_code = VERIFICATION_CODES[ctx.author.id]

        if code == correct_code:
            role = discord.utils.get(ctx.guild.roles, name="etudiant")
            await ctx.author.add_roles(role)
            await ctx.send("Votre compte a été vérifié et vous avez reçu le rôle Étudiant.")
            del VERIFICATION_CODES[ctx.author.id]
        else:
            await ctx.send("Le code est incorrect. Veuillez réessayer.")

async def setup(bot):
    await bot.add_cog(Verification(bot))
