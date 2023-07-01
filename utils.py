# STL
from typing import Optional

# PDM
import discord
from discord.ext.commands.errors import RoleNotFound, UserNotFound

# LOCAL
from logger import LOG

discord.Guild


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
