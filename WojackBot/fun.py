# STL
import os
import logging

# PDM
import discord
from dotenv import load_dotenv
from discord.ext import tasks, commands

# LOCAL
from .utils.discord_utils import make_get_request, select_random_hero

discord.Member
LOG = logging.getLogger()
load_dotenv()

CHANNEL = os.getenv("CHANNEL_ID")
USER = os.getenv("USER_ID")


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.looped_task.start()
        self.heroes = ""

    def cog_unload(self):
        self.looped_task.cancel()

    @tasks.loop(
        seconds=3600
    )  # Adjust the interval as desired (currently set to 1 hour).
    async def looped_task(self):
        channel_id = int(
            CHANNEL
        )  # Replace this with the ID of the channel where you want the command to run periodically.
        channel = self.bot.get_channel(channel_id)
        if channel:
            if member := channel.guild.get_member(int(USER)):
                await member.edit(nick=f"{select_random_hero(self.heroes)} main")

    @looped_task.before_loop
    async def before_looped_task(self):
        await self.bot.wait_until_ready()
        self.heroes = await make_get_request("https://overfast-api.tekrop.fr/heroes")
