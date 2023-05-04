# PDM
import discord
from gpt4free import you
from discord.ext import commands


class GPT(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.slash_command(name="ask_gpt")
    async def ask_gpt(
        self, ctx, question: discord.Option(str, description="Ask ChatGPT something.")
    ):
        # Send initial message to let the user know that their request is being processed
        await ctx.respond(f"Question: {question}")

        # Generate the response
        response = you.Completion.create(prompt=question)

        await ctx.send(response.text)
