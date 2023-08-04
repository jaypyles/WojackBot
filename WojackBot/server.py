# PDM
import discord
from discord.ext import commands
from discord.ext.pages import Page, Paginator, PaginatorMenu, PaginatorButton

# LOCAL
from WojackBot.utils.discord_utils import find_role_by_query, find_user_by_query

# LOCAL
from .logger import LOG

Games = {"op1": "BattleBit", "op2": "Overwatch", "op3": "Rocket League"}

GameImages = {
    "Overwatch": "https://news.xbox.com/en-us/wp-content/uploads/sites/2/2022/10/OW2-be9287b234afbe7898ac.jpg",
    "BattleBit": "https://pbs.twimg.com/profile_images/1667969937762131970/1Z8mfNOW_400x400.jpg",
    "Rocket League": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCqkTzsQmelU0Pshc-O5AjDJk0D854mJgWzdx5b5gHlpL5I5srMZvTB1oeKncfoPS4V5M&usqp=CAU",
}


class Select(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="BattleBit", emoji="🔫", value="op1"),
            discord.SelectOption(label="Overwatch", emoji="🐉", value="op2"),
            discord.SelectOption(label="Rocket League", emoji="🚗", value="op3"),
        ]
        super().__init__(
            placeholder="Game", max_values=1, min_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(interaction.channel_id)

        self.game = self.values[0]

        embed = discord.Embed(
            title="Looking for Gamers!",
            description=f"{interaction.user.mention} is looking for {Games[self.game]}r's!",
            color=discord.Color.blue(),
        )

        embed.set_image(url=GameImages[Games[self.game]])
        await channel.send(content="@here", embed=embed)


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180, bot):
        self.bot = bot
        super().__init__(timeout=timeout)
        self.add_item(Select(self.bot))


class ServerCommands(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    server_commmands = discord.SlashCommandGroup("server_commmands")

    @server_commmands.command(
        name="gamer_search",
        description="Send annoucment that you are looking for gamers.",
    )
    async def game_annoucement(self, ctx):
        await ctx.respond(
            "Select a game:", view=SelectView(bot=self.bot), ephemeral=True
        )

    @server_commmands.command(
        name="purge_messages", description="Purge messages up to a set limit."
    )
    @commands.has_guild_permissions(manage_messages=True)
    async def purge_messages(self, ctx, message_amount: discord.Option(int, description="amount of messages")):  # type: ignore
        await ctx.respond(f"Purging {message_amount} message(s)...", ephemeral=True)
        await ctx.channel.purge(limit=message_amount + 1)

    @purge_messages.error
    async def purge_messages_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(
                "You do not have the required permissions to use this command.",
                ephemeral=True,
            )

    @server_commmands.command(
        name="assign_role", description="Assign a role to a member."
    )
    @commands.has_permissions(manage_permissions=True, manage_roles=True)
    async def assign_role(
        self,
        ctx,
        role_name: discord.Option(str, description="role to assign"),  # type: ignore
        username: discord.Option(str, description="user to assign to"),  # type: ignore
        user_id: discord.Option(  # type: ignore
            str, description="user id to assign to", required=False
        ),
    ):
        if user_id:
            member = await find_user_by_query(ctx, username=username, user_id=[user_id])
        else:
            member = await find_user_by_query(ctx, username=username)
        role = await find_role_by_query(ctx, role_name=role_name)

        if role:
            if member:
                await member.add_roles(role)
                await ctx.respond(
                    f"Member: {member} was given role: {role_name}", ephemeral=True
                )
            else:
                await ctx.respond(f"Member: {member}, not found.", ephemeral=True)
        else:
            await ctx.respond(f"Role: {role_name}, not found.", ephemeral=True)

    @server_commmands.command(
        name="remove_role", description="Remove a role from a member."
    )
    @commands.has_permissions(manage_permissions=True, manage_roles=True)
    async def remove_role(
        self,
        ctx,
        role_name: discord.Option(str, description="role to remove"),  # type: ignore
        username: discord.Option(str, description="user to remove from"),  # type: ignore
        user_id: discord.Option(  # type: ignore
            str, description="user id to assign to", required=False
        ),
    ):
        if user_id:
            member = await find_user_by_query(ctx, username=username, user_id=[user_id])
        else:
            member = await find_user_by_query(ctx, username=username)
        role = await find_role_by_query(ctx, role_name=role_name)

        if role:
            if member:
                await member.remove_roles(role)
                await ctx.respond(
                    f"Member: {member} was given role: {role_name}", ephemeral=True
                )
            else:
                await ctx.respond(f"Member: {member}, not found.", ephemeral=True)
        else:
            await ctx.respond(f"Role: {role_name}, not found.", ephemeral=True)

    @server_commmands.command(name="make_role", description="Create a role.")
    @commands.has_permissions(manage_permissions=True, manage_roles=True)
    async def create_role(self, ctx, role_name: discord.Option(str, description="role to create")):  # type: ignore
        guild = ctx.guild
        role = await guild.create_role(name=role_name)
        await ctx.respond(f"Role: {role}, created...", ephemeral=True)

    @server_commmands.command(name="delete_role", description="Delete a role.")
    @commands.has_permissions(manage_permissions=True, manage_roles=True)
    async def delete_role(self, ctx, role_name: discord.Option(str, description="role to delete")):  # type: ignore
        role = discord.utils.get(ctx.guild.roles, name=role_name)  # type: ignore
        if role:
            await role.delete()
            await ctx.respond(f"Role: {role}, deleted...", ephemeral=True)
        else:
            await ctx.respond(f"Role: {role_name}, not found", ephemeral=True)

    @server_commmands.command(
        name="give_role_permissions", description="Give permissions to a role."
    )
    @commands.has_permissions(manage_permissions=True, manage_roles=True)
    async def give_role_permissions(self, ctx, role_name: discord.Option(str, description="role to give permissions to"), perms: discord.Option(str, description="permission list")):  # type: ignore
        set_permissions = []
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        permission_list = perms.split(" ")

        permissions = discord.Permissions()

        for permission in permission_list:
            try:
                setattr(permissions, permission, True)
                set_permissions.append(permission)
            except:
                await ctx.respond(f"{permission} does not exist.")

        await role.edit(permissions=permissions)
        await ctx.respond(
            f"Role: {role_name}, {set_permissions} set to True.", ephemeral=True
        )

    @server_commmands.command(
        name="delete_role_permissions", description="Remove permissions from a role."
    )
    @commands.has_permissions(manage_permissions=True, manage_roles=True)
    async def remove_role_permissions(self, ctx, role_name: discord.Option(str, description="role to remove permissions from"), perms: discord.Option(str, description="permission list")):  # type: ignore
        remove_permissions = []
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        permission_list = perms.split(" ")

        permissions = discord.Permissions()

        for permission in permission_list:
            try:
                setattr(permissions, permission, False)
                remove_permissions.append(permission)
            except:
                await ctx.respond(f"{permission} does not exist.", ephemeral=True)

        await role.edit(permissions=permissions)
        await ctx.respond(
            f"Role: {role_name}, {remove_permissions} set to False.", ephemeral=True
        )
