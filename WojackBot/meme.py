# STL
import os
import time

# PDM
import discord
import gpt4free
import ifunnygifmaker
from dotenv import load_dotenv
from gpt4free import Provider
from discord.ext import commands

# LOCAL
from WojackBot.utils.checks import validate_caption
from WojackBot.utils.constants import MAX_RETRIES, ERROR_MESSAGE
from WojackBot.utils.meme_utils import gather_prompt_text
from WojackBot.utils.transformers import caption_strip

# LOCAL
from .logger import LOG

# FUNCTIONAL
load_dotenv()
tenor_token = os.getenv("TENOR_API_KEY")
m = ifunnygifmaker.MemeMaker(token=tenor_token)


def create_meme_caption():
    """Resolve a meme caption from the GPT4FREE API"""
    prompt = "Reply with a 5 word caption for a random meme, something that is relatable, do not include quotations or any sort of punctuation like periods, commas, etc."
    retries = 0
    while retries < MAX_RETRIES:
        response = gpt4free.Completion.create(Provider.You, prompt=prompt)
        caption = caption_strip(response)
        if validate_caption(caption):
            return caption
        else:
            LOG.warning(
                f"Invalid caption: {caption}. Retrying... ({retries+1}/{MAX_RETRIES})"
            )
            retries += 1
            time.sleep(1)

    return ERROR_MESSAGE


def create_meme_prompted_caption(prompt):
    """Resolve a meme caption from the GPT4FREE api"""
    prompt = gather_prompt_text("prompts/memeprompt.txt") + prompt
    retries = 0
    while retries < MAX_RETRIES:
        response = gpt4free.Completion.create(Provider.You, prompt=prompt)
        caption = caption_strip(response)
        if validate_caption(caption):
            return caption
        else:
            LOG.warning(
                f"Invalid caption: {caption}. Retrying... ({retries+1}/{MAX_RETRIES})"
            )
            retries += 1
            time.sleep(1)

    return ERROR_MESSAGE


def create_meme_gif(caption):
    """Resolve a gif caption from the GPT4FREE api"""
    prompt = f"Reply with a 2 word idea for a gif that would go with this meme: {caption}, do not include quotations or any sort of punctuation."
    response = gpt4free.Completion.create(Provider.You, prompt=prompt)
    return response


class MemeMaking(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    meme_making = discord.SlashCommandGroup("meme_making")

    @meme_making.command(name="random", description="Generate a random meme")
    async def random(self, ctx):
        await ctx.respond("Making a meme..", ephemeral=True)

        caption = create_meme_caption()
        if caption == ERROR_MESSAGE:
            await ctx.respond("Meme could not be created, try again.", ephemeral=True)
            return

        search = create_meme_gif(caption)

        LOG.info("Making meme with [caption: %s], [query: %s]", caption, search)
        m.make_meme(text=caption, query=search.replace(" ", "+"))
        with open("out.gif", "rb") as f:
            file = discord.File(f)

        embed = discord.Embed(title="prompt: random")
        embed.set_image(url="attachment://out.gif")
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
        caption = create_meme_prompted_caption(prompt)

        if caption == ERROR_MESSAGE:
            await ctx.respond("Meme could not be created, try again.", ephemeral=True)
            return

        search = create_meme_gif(caption)

        m.make_meme(text=caption, query=search.replace(" ", "+"))
        with open("out.gif", "rb") as f:
            file = discord.File(f)

        embed = discord.Embed(title=f"prompt: {prompt}")
        embed.set_image(url="attachment://out.gif")
        await ctx.send(file=file, embed=embed)
