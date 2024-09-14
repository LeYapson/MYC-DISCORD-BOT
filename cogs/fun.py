import random
import discord
from discord.ext import commands
import asyncio
import datetime

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='flip')
    async def flip_coin(self, ctx):
        """Commande pour lancer une pièce (pile ou face)."""
        result = random.choice(['Pile', 'Face'])
        await ctx.send(f"La pièce tombe sur : {result}!")

    @commands.command(name='roll')
    async def roll_dice(self, ctx, sides: int = 6):
        """Commande pour lancer un dé avec un nombre de faces spécifié (par défaut 6)."""
        if sides < 1:
            await ctx.send("Le nombre de faces doit être supérieur à 0.")
            return
        result = random.randint(1, sides)
        await ctx.send(f"Vous avez lancé un dé à {sides} faces et obtenu : {result}")

    @commands.command(name='blog')
    async def blog(self, ctx):
        """Commande pour obtenir une URL de blog aléatoire."""
        urls = [
            "https://theauyapi-portfolio.netlify.app",
            "https://www.axel.fun",
            "https://chickenonaraft.com",
            "https://perdu.com"
        ]
        url = random.choice(urls)
        await ctx.send(f"Découvrez ce blog intéressant : {url}")

    @commands.command(name='bobdell')
    async def random_quote(self, ctx):
        """Commande pour afficher une image au format géant."""
        image_url = "https://leyapson.github.io/MYC-DISCORD-BOT/bobdell.html"  # Remplacez cette URL par celle de votre image
        embed = discord.Embed(title="Image Géante")
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    
    @commands.command(name='apagnan')
    async def apagnan(self, ctx):
        """Commande pour faire crier le bot 'YNOV CEST UNE GRANDE FAMILLE' plusieurs fois pendant 20 secondes."""
        if self.repeat_task and not self.repeat_task.done():
            await ctx.send("La commande est déjà en cours.")
            return

        async def repeat_message():
            end_time = discord.utils.utcnow() + datetime.timedelta(seconds=20)
            while discord.utils.utcnow() < end_time:
                await ctx.send("YNOV CEST UNE GRANDE FAMILLE")
                await asyncio.sleep(2)  # Envoie le message toutes les 2 secondes

        self.repeat_task = asyncio.create_task(repeat_message())

async def setup(bot):
    await bot.add_cog(Fun(bot))