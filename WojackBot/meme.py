# STL
import os

# PDM
import discord
import ifunnygifmaker
from dotenv import load_dotenv
from discord.ext import commands

# LOCAL
from .utils import create_meme_gif, create_meme_caption
from .logger import LOG

# FUNCTIONAL
load_dotenv()
tenor_token = os.getenv("TENOR_API_KEY")
m = ifunnygifmaker.MemeMaker(token=tenor_token)


class MemeMaking(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    meme_making = discord.SlashCommandGroup("meme_making")

    @meme_making.command(name="random", help="Generate a random meme")
    async def random(self, ctx):
        await ctx.respond("Making random meme..")

        caption = create_meme_caption()
        search = create_meme_gif(caption)

        LOG.info("Making meme with [caption: %s], [query: %s]", caption, search)
        m.make_meme(text=caption, query=search.replace(" ", "+"))
        with open("out.gif", "rb") as f:
            file = discord.File(f)

        embed = discord.Embed(title="woah funny!")
        embed.set_image(url="attachment://out.gif")
        await ctx.send(file=file, embed=embed)

    @meme_making.command(name="construct_meme", help="Construct a meme.")
    async def meme(
        self,
        ctx,
        caption: discord.Option(str, description="Caption for your meme."),  # type: ignore
        url: discord.Option(str, description="The url of the Tenor media gif."),  # type: ignore
    ):
        await ctx.respond("Making a meme..")

        m.make_meme(text=caption, url=url)
        with open("out.gif", "rb") as f:
            file = discord.File(f)

        embed = discord.Embed(title="woah funny!")
        embed.set_image(url="attachment://out.gif")
        await ctx.send(file=file, embed=embed)