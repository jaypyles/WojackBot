# STL
import os

# PDM
import discord
import ifunnygifmaker
from dotenv import load_dotenv

# LOCAL
from gpt import GPT
from reddit import RedditSearcher

# LOAD ENV
load_dotenv()
token = os.getenv("TOKEN")
tenor_token = os.getenv("TENOR_API_KEY")

# FUNCTIONAL
m = ifunnygifmaker.MemeMaker(token=tenor_token)
reddit = RedditSearcher()
caption_subreddit = reddit.subreddit("copypasta")
meme_generation = reddit.subreddit("gif")


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.typing = True
bot = discord.Bot(command_prefix="**", intents=intents)
bot.add_cog(GPT(bot))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("doom scrolling"))
    print(f"Logged in as {bot.user}")


meme_making = bot.create_group("meme_making", "Commands related to making memes")


@meme_making.command(name="random", description="Generate random meme.")
async def random(ctx):
    await ctx.respond("Making random meme..")

    caption = caption_subreddit.random().title
    search = meme_generation.random().title

    m.make_meme(text=caption, query=search.replace(" ", "+"))
    with open("out.gif", "rb") as f:
        file = discord.File(f)

    await ctx.send(file=file)


@meme_making.command()
async def meme(
    ctx,
    caption: discord.Option(str, description="Caption for your meme."),
    url: discord.Option(str, description="The url of the Tenor media gif."),
):
    await ctx.respond("Making a meme..")

    m.make_meme(text=caption, url=url)
    with open("out.gif", "rb") as f:
        file = discord.File(f)

    await ctx.send(file=file)


bot.run(token)
