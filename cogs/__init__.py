from .roles import Roles
from .moderation import Moderation
from .utils import Utils
from .verification import Verification

async def setup(bot):
    # Ajouter les cogs ici, uniquement une fois
    await bot.add_cog(Roles(bot))
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(Utils(bot))
    await bot.add_cog(Verification(bot))
