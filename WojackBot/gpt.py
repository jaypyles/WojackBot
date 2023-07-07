# PDM
import discord
import gpt4free
from gpt4free import Provider
from discord.ext import commands

# LOCAL
from .logger import LOG


class GPT(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    gpt = discord.SlashCommandGroup("ask_chatgpt")

    @gpt.command(
        name="normal_prompt", description="Give a prompt, and the bot will respond."
    )
    async def normal_prompt(
        self, ctx, prompt: discord.Option(str, description="Ask ChatGPT something.")  # type: ignore
    ):
        await ctx.respond(f"Prompt: {prompt}")
        LOG.info("Prompt: %s", prompt)
        response = gpt4free.Completion.create(Provider.You, prompt=prompt)

        await ctx.send(response)
