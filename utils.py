# STL
from typing import Optional

# PDM
import discord
import gpt4free
from gpt4free import Provider
from discord.ext.commands.errors import RoleNotFound, UserNotFound

# LOCAL
from logger import LOG


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


def create_meme_caption():
    """Resolve a meme caption from the GPT4FREE api"""
    prompt = "Reply with a 5 word caption for a meme, do not include quotations or any sort of punctuation like periods, commas, etc."
    response = gpt4free.Completion.create(Provider.You, prompt=prompt)
    return response


def create_meme_gif(caption):
    """Resolve a gif caption from the GPT4FREE api"""
    prompt = f"Reply with a 5 word idea for a gif that would go with this meme: {caption}, do not include quotations or any sort of punctuation."
    response = gpt4free.Completion.create(Provider.You, prompt=prompt)
    return response
