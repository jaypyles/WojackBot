# STL
import random
from typing import Optional

# PDM
import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands.errors import RoleNotFound, UserNotFound

# LOCAL
from WojackBot.logger import LOG


class Select(discord.ui.Select):
    def __init__(self, options: list, placeholder: str):
        options = options
        super().__init__(
            placeholder=placeholder, max_values=1, min_values=1, options=options
        )


class SelectView(discord.ui.View):
    """A select menu that can be sent as a view"""

    def __init__(self, options: list, placeholder: str, timeout=180):
        super().__init__(timeout=180)
        self.add_item(Select(options, placeholder))


async def get_cog_commands(bot: commands.Bot, cog: discord.Cog):
    """Get all commands that belong to a certain Cog for a Bot"""
    cog_commands = []
    for command in bot.commands:
        if command.cog and command.cog.qualified_name == cog:
            cog_commands.append(command)

    return cog_commands


async def get_cogs(bot: discord.Bot):
    """Get a list of all cogs loaded into a Bot"""
    return [key for key in bot.cogs.keys()]


async def find_user_by_query(
    ctx, username: str, user_id: Optional[list[str]] = None
) -> discord.Member:
    """Find user in a guild by username"""
    if user_id:
        queried_members = await ctx.guild.query_members(user_ids=user_id)
    else:
        queried_members = await ctx.guild.query_members(query=username)

    member = next((mem for mem in queried_members if mem.name == username), None)

    if member is not None:
        return member
    else:
        raise UserNotFound(username)


async def find_role_by_query(ctx, role_name: str) -> discord.Role:
    """Find role by name"""
    roles = await ctx.guild.fetch_roles()

    role = next((r for r in roles if r.name == role_name))

    if role is not None:
        return role
    else:
        raise RoleNotFound(role_name)


async def make_get_request(url):
    """Make an async get request"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


def select_random_hero(heroes):
    """Select a random hero from a list of heroes"""
    rand = random.randrange(0, len(heroes) - 1)
    return heroes[rand].get("key")


async def send_used_command(ctx):
    """Message the command that was used."""
    await ctx.send(f"{ctx.user.mention} used: {ctx.command}")
