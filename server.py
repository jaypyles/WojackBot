# PDM
import discord
from discord.ext import commands

# LOCAL
from logger import LOG

Games = {
    "op1": "BattleBit",
    "op2": "Overwatch",
    "op3": "Rocket League"
}

GameImages = {
    "Overwatch": "https://news.xbox.com/en-us/wp-content/uploads/sites/2/2022/10/OW2-be9287b234afbe7898ac.jpg",
    "BattleBit": "https://pbs.twimg.com/profile_images/1667969937762131970/1Z8mfNOW_400x400.jpg",
    "Rocket League": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCqkTzsQmelU0Pshc-O5AjDJk0D854mJgWzdx5b5gHlpL5I5srMZvTB1oeKncfoPS4V5M&usqp=CAU"
}

class Select(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options=[
            discord.SelectOption(label="BattleBit",emoji="🔫", value="op1"),
            discord.SelectOption(label="Overwatch", emoji="🐉", value="op2"),
            discord.SelectOption(label="Rocket League", emoji="🚗", value="op3")
            ]
        super().__init__(placeholder="Game",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(interaction.channel_id)

        self.game = self.values[0]

        embed = discord.Embed(
            title="Looking for Gamers!",
            description=f"{interaction.user.mention} is looking for {Games[self.game]}r's!",
            color=discord.Color.blue()
        )

        embed.set_image(url=GameImages[Games[self.game]])
        await channel.send(content="@here", embed=embed)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot):
        self.bot = bot
        super().__init__(timeout=timeout)
        self.add_item(Select(self.bot))

class ServerCommands(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    server_commmands = discord.SlashCommandGroup("server_commmands")

    @server_commmands.command(name="gamer_search", description="Send annoucment that you are looking for gamers.")
    async def game_annoucement(self, ctx):
        await ctx.respond("Select a game:",view=SelectView(bot=self.bot), ephemeral=True)

    @server_commmands.command(name="purge_messages", description="Purge messages up to a set limit.")
    @commands.has_guild_permissions(administrator=True)
    async def purge_messages(self, ctx, message_amount: discord.Option(int, description="amount of messages")): #type: ignore
        await ctx.respond(f"Purging {message_amount} message(s)...", ephemeral=True)
        await ctx.channel.purge(limit=message_amount+1)

    @purge_messages.error
    async def purge_messages_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You do not have the required permissions to use this command.", ephemeral=True)
