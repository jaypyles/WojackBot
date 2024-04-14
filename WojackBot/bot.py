# STL
import os

# PDM
import discord
from dotenv import load_dotenv
from discord.ext import commands

# LOCAL
from WojackBot.search import SearchCommands
from WojackBot.utils.discord_utils import SelectView, get_cogs

# LOCAL
from .fun import Fun
from .gpt import GPT
from .meme import MemeMaking
from .server import ServerCommands

# LOAD ENV
load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.typing = True
intents.members = True
bot = commands.Bot(command_prefix="**", intents=intents)

# Cogs
bot.add_cog(GPT(bot))
bot.add_cog(ServerCommands(bot))
bot.add_cog(MemeMaking(bot))
bot.add_cog(Fun(bot))
bot.add_cog(SearchCommands(bot))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("doom scrolling"))
    print(f"Logged in as {bot.user}")


@bot.slash_command(name="help", description="Get information about all commands.")
async def help(ctx):
    help_embed = discord.Embed(
        title="WojackBot's Commands",
        description="A list of all of the commands that the WojackBot provides.",
        color=discord.Color.greyple(),
    )
    help_embed.set_image(url=str(bot.user.avatar))
    help_embed.set_footer(text="Select a command group from the menu below.")

    cogs = await get_cogs(bot)
    options = [discord.SelectOption(label=cog, value=cog) for cog in cogs]

    select = SelectView(options=options, placeholder="Select a command group:")

    await ctx.respond(embed=help_embed)
    await ctx.send(view=select)


@bot.message_command(name="Make Meme")
async def get_message_text(ctx, message: discord.Message):
    await bot.get_cog("MemeMaking").make_message_meme(ctx, message.content)


bot.run(token)
