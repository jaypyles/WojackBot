# STL
import os
import time

# PDM
import g4f
import discord
import ifunnygifmaker
from dotenv import load_dotenv
from discord.ext import commands

# LOCAL
from WojackBot.utils.ai import call_ai
from WojackBot.utils.checks import validate_gif, validate_caption
from WojackBot.utils.constants import MAX_RETRIES, ERROR_MESSAGE
from WojackBot.utils.meme_utils import gather_prompt_text
from WojackBot.utils.transformers import caption_strip
from WojackBot.utils.discord_utils import send_used_command

# LOCAL
from .logger import LOG

# FUNCTIONAL
load_dotenv()
tenor_token = os.getenv("TENOR_API_KEY")
m = ifunnygifmaker.MemeMaker(token=tenor_token)


async def create_meme_caption():
    """Resolve a meme caption from the GPT4FREE API"""
    prompt = "Reply with a 5 word caption for a random meme, something that is relatable, do not include quotations or any sort of punctuation like periods, commas, etc."
    retries = 0
    while retries < MAX_RETRIES:
        response = await call_ai(prompt)
        caption = caption_strip(response)
        if validate_caption(caption):
            return caption
        else:
            LOG.warning(
                f"Invalid caption: {caption}. Retrying... ({retries+1}/{MAX_RETRIES})"
            )
            retries += 1
            time.sleep(3)

    return ERROR_MESSAGE


async def create_meme_prompted_caption(prompt):
    """Resolve a meme caption from the GPT4FREE api"""
    prompt = gather_prompt_text("prompts/memeprompt.txt") + prompt
    retries = 0
    while retries < MAX_RETRIES:
        response = await call_ai(prompt)
        caption = caption_strip(response)
        if validate_caption(caption):
            return caption
        else:
            LOG.warning(
                f"Invalid caption: {caption}. Retrying... ({retries+1}/{MAX_RETRIES})"
            )
            retries += 1
            time.sleep(3)

    return ERROR_MESSAGE


async def create_meme_gif(caption):
    """Resolve a gif caption from the GPT4FREE api"""
    prompt = f"Reply with a 2-3 word idea for a gif that would go with this meme: {caption}, do not include quotations or any sort of punctuation."
    retries = 0
    while retries < MAX_RETRIES:
        response = await call_ai(prompt)
        if validate_gif(response):
            return response
        else:
            LOG.warning(
                f"Invalid gif query: {response}. Retrying... ({retries+1}/{MAX_RETRIES})"
            )
            retries += 1
            time.sleep(3)

    return ERROR_MESSAGE


class MemeMaking(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def make_message_meme(self, ctx, message_content: str):
        await ctx.respond("Making a meme..", ephemeral=True)
        caption = await create_meme_prompted_caption(prompt=message_content)
        if caption == ERROR_MESSAGE:
            await ctx.respond("Meme could not be created, try again.", ephemeral=True)
            return

        search = create_meme_gif(caption)
        if search == ERROR_MESSAGE:
            await ctx.respond("Meme could not be created, try again.", ephemeral=True)
            return

        LOG.info("Making meme with [caption: %s], [query: %s]", caption, search)
        m.make_meme(text=caption, query=search.replace(" ", "+"))
        with open("out.gif", "rb") as f:
            file = discord.File(f)

        embed = discord.Embed(
            title="prompt: message content", description=f"Message: {message_content}"
        )

        embed.set_image(url="attachment://out.gif")
        await send_used_command(ctx)
        await ctx.send(file=file, embed=embed)

    meme_making = discord.SlashCommandGroup("meme_making")

    @meme_making.command(name="random", description="Generate a random meme")
    async def random(self, ctx):
        await ctx.respond("Making a meme..", ephemeral=True)

        caption = await create_meme_caption()
        if caption == ERROR_MESSAGE:
            await ctx.respond("Meme could not be created, try again.", ephemeral=True)
            return

        search = create_meme_gif(caption)
        if search == ERROR_MESSAGE:
            await ctx.respond("Meme could not be created, try again.", ephemeral=True)
            return

        LOG.info("Making meme with [caption: %s], [query: %s]", caption, search)
        m.make_meme(text=caption, query=search.replace(" ", "+"))
        with open("out.gif", "rb") as f:
            file = discord.File(f)

        embed = discord.Embed(title="prompt: random")
        embed.set_image(url="attachment://out.gif")
        await send_used_command(ctx)
        await ctx.send(file=file, embed=embed)

    @meme_making.command(name="construct_meme", description="Construct a meme.")
    async def meme(
        self,
        ctx,
        caption: discord.Option(str, description="Caption for your meme."),  # type: ignore
        url: discord.Option(str, description="The url of the Tenor media gif."),  # type: ignore
    ):
        await ctx.respond("Making a meme..", ephemeral=True)

        m.make_meme(text=caption, url=url)
        with open("out.gif", "rb") as f:
            file = discord.File(f)

        embed = discord.Embed(title=f"prompt: {caption}")
        embed.set_image(url="attachment://out.gif")
        await send_used_command(ctx)
        await ctx.send(file=file, embed=embed)

    @meme_making.command(
        name="prompt_meme", description="Construct a meme from a prompt."
    )
    async def prompted_meme(
        self,
        ctx,
        prompt: discord.Option(str, description="Prompt for your meme."),  # type: ignore
    ):
        await ctx.respond("Making a meme..", ephemeral=True)
        caption = await create_meme_prompted_caption(prompt)
        LOG.info(f"caption: {caption}")

        if caption == ERROR_MESSAGE:
            await ctx.respond("Meme could not be created, try again.", ephemeral=True)
            return

        search = create_meme_gif(caption)
        if search == ERROR_MESSAGE:
            await ctx.respond("Meme could not be created, try again.", ephemeral=True)
            return

        m.make_meme(text=caption, query=search.replace(" ", "+"))
        with open("out.gif", "rb") as f:
            file = discord.File(f)

        embed = discord.Embed(title=f"prompt: {prompt}")
        embed.set_image(url="attachment://out.gif")
        await send_used_command(ctx)
        await ctx.send(file=file, embed=embed)
