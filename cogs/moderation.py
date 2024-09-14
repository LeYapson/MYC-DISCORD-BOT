from discord.ext import commands
from discord import Member, Role
from datetime import timedelta
import asyncio
import json
import os

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = os.path.join('data', 'infractions.json')

    # Commande pour purge les messages
    @commands.command(name='purge')
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount: int):
        """Commande pour supprimer un nombre spécifique de messages."""
        if amount < 1:
            await ctx.send("Vous devez spécifier un nombre positif de messages à supprimer.")
            return
        elif amount > 100:
            await ctx.send("Vous ne pouvez pas supprimer plus de 100 messages à la fois.")
            return
        
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"{len(deleted)} messages supprimés.", delete_after=5)

    # Commande pour expulser un utilisateur
    @commands.command(name='kick')

    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        """Commande pour expulser un utilisateur."""
        await member.kick(reason=reason)
        await ctx.send(f"{member} a été expulsé pour la raison : {reason}")

    # Commande pour bannir un utilisateur
    @commands.command(name='ban')

    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason=None):
        """Commande pour bannir un utilisateur."""
        await member.ban(reason=reason)
        await ctx.send(f"{member} a été banni pour la raison : {reason}")

    # Commande pour débannir un utilisateur
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member_name):
        """Commande pour débannir un utilisateur."""
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == member_name:
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name} a été débanni.")
                return
        await ctx.send(f"L'utilisateur {member_name} n'a pas été trouvé dans la liste des bannis.")

    # Commande pour mute un utilisateur
    @commands.command(name='mute')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Member, duration: int, *, reason=None):
        """Commande pour mute un utilisateur pour une durée spécifique."""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            # Crée un rôle Muted si celui-ci n'existe pas
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False, speak=False)
        
        await member.add_roles(role)
        await ctx.send(f"{member.mention} a été mute pour {duration} minutes. Raison : {reason}")
        await asyncio.sleep(duration * 60)
        await member.remove_roles(role)

    # Commande pour unmute un utilisateur
    @commands.command(name='unmute')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: Member):
        """Commande pour unmute un utilisateur."""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"{member.mention} n'est plus mute.")
        else:
            await ctx.send(f"{member.mention} n'est pas mute.")

    # Commande pour avertir un utilisateur
    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: Member, *, reason=None):
        """Commande pour avertir un utilisateur."""
        await ctx.send(f"{member.mention} a reçu un avertissement pour la raison : {reason}")

    # Commande pour appliquer un slowmode sur un canal
    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        """Commande pour appliquer un slowmode sur un canal."""
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Le slowmode a été défini à {seconds} secondes.")

    # Commande pour verrouiller un canal
    @commands.command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        """Commande pour verrouiller un canal."""
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"Le canal {ctx.channel.name} est maintenant verrouillé.")

    # Commande pour déverrouiller un canal
    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        """Commande pour déverrouiller un canal."""
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"Le canal {ctx.channel.name} est maintenant déverrouillé.")

    # Commande pour bannir temporairement un utilisateur
    @commands.command(name='tempban')
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: Member, duration: int, *, reason=None):
        """Commande pour bannir temporairement un utilisateur."""
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} a été banni pour {duration} minutes. Raison : {reason}")
        await asyncio.sleep(duration * 60)
        await ctx.guild.unban(member)

    # Commande pour changer le pseudo d'un utilisateur
    @commands.command(name='nick')
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: Member, *, nickname):
        """Commande pour changer le pseudo d'un utilisateur."""
        await member.edit(nick=nickname)
        await ctx.send(f"Le pseudo de {member.mention} a été changé en {nickname}.")

    @commands.command(name='infractions')
    @commands.has_permissions(manage_messages=True)
    async def infractions(self, ctx, member: Member):
        """Commande pour consulter les infractions d'un utilisateur."""
        user_id = str(member.id)
        
        # Lecture du fichier JSON
        if not os.path.isfile(self.data_file):
            await ctx.send("Le fichier des infractions n'a pas été trouvé.")
            return
        
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            await ctx.send("Erreur de lecture du fichier des infractions.")
            return
        
        # Récupération des infractions
        infractions = data.get(user_id, [])
        
        # Formatage des infractions en une chaîne de caractères
        if infractions:
            infractions_list = "\n".join(infractions)
            message = f"Consultation des infractions pour {member.mention} :\n{infractions_list}"
        else:
            message = f"Aucune infraction trouvée pour {member.mention}."
        
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
