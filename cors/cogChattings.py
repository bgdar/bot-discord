from discord.ext import commands
import discord


class CogChattings(commands.Cog):
    """chating biasa dengan bot"""

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        super().__init__()

    # --- Bot Listener start
    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member):
        """sapa Member Join"""
        chanel = member.guild.system_channel()
        if chanel:
            await member.send(f"Welcome to the server {member.mention}")

    # ada  yang default nya
    # @commands.command(name="help")
    # async def help(self, ctx: commands.Context, *, member: discord.Member = None):
    #     """Commadn Bantuan untuk Chattings"""
    #     await ctx.send("Just chattings with me ")
