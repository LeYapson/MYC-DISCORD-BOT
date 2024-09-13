import discord
import asyncio

async def add_reaction_with_rate_limit(message, emoji):
    try:
        await message.add_reaction(emoji)
    except discord.HTTPException as e:
        if e.code == 429:
            retry_after = e.retry_after
            print(f"Rate limited. Retrying after {retry_after} seconds.")
            await asyncio.sleep(retry_after)
            await add_reaction_with_rate_limit(message, emoji)
