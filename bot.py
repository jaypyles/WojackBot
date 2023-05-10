# STL
import os

# PDM
import discord
from dotenv import load_dotenv

# LOCAL
from gpt import GPT
from meme import MemeMaking

# LOAD ENV
load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.typing = True
bot = discord.Bot(command_prefix="**", intents=intents)
bot.add_cog(GPT(bot))
bot.add_cog(MemeMaking(bot))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("doom scrolling"))
    print(f"Logged in as {bot.user}")


bot.run(token)
