from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        if amount < 1:
            await ctx.send("Vous devez spécifier un nombre positif de messages à supprimer.")
            return
        elif amount > 100:
            await ctx.send("Vous ne pouvez pas supprimer plus de 100 messages à la fois.")
            return
        
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"{len(deleted)} messages supprimés.", delete_after=5)

def setup(bot):
    bot.add_cog(Moderation(bot))
