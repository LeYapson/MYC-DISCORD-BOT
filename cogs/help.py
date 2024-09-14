import discord
from discord.ext import commands

class MyHelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'help': "Affiche ce message d'aide."
        })

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Commandes du bot",
            description="Voici la liste des commandes disponibles :",
            color=discord.Color.blurple()
        )
        
        for cog, commands in mapping.items():
            if cog is None:
                continue
            filtered = await self.filter_commands(commands, sort=True)
            if not filtered:
                continue
            cog_name = cog.qualified_name if cog else "Autres"
            command_list = "\n".join([f"`{self.context.clean_prefix}{command.name}`: {command.help}" for command in filtered])
            embed.add_field(name=f"**{cog_name}**", value=command_list, inline=False)

        embed.set_footer(text=f"Utilise {self.context.clean_prefix}help <commande> pour plus de détails.")
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"Aide pour la commande `{self.context.clean_prefix}{command.name}`",
            description=command.help or "",
            color=discord.Color.green()
        )
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(f"`{alias}`" for alias in command.aliases), inline=False)
        embed.add_field(name="Usage", value=self.get_command_signature(command), inline=False)
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(
            title=f"Aide pour le groupe de commandes `{self.context.clean_prefix}{group.name}`",
            description=group.help or "",
            color=discord.Color.orange()
        )
        if group.aliases:
            embed.add_field(name="Aliases", value=", ".join(f"`{alias}`" for alias in group.aliases), inline=False)
        embed.add_field(name="Sous-commandes", value="\n".join(f"`{self.context.clean_prefix}{c.name}`: {c.help}" for c in group.commands), inline=False)
        embed.add_field(name="Usage", value=self.get_command_signature(group), inline=False)
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f"Aide pour la catégorie `{cog.qualified_name}`",
            description=cog.description or "",
            color=discord.Color.purple()
        )
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        if filtered:
            command_list = "\n".join(f"`{self.context.clean_prefix}{command.name}`: {command.help}" for command in filtered)
            embed.add_field(name="Commandes", value=command_list, inline=False)
        await self.get_destination().send(embed=embed)

    def get_command_signature(self, command):
        return f"`{self.context.clean_prefix}{command.qualified_name} {command.signature}`"


class Help(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


async def setup(bot):
    await bot.add_cog(Help(bot))
