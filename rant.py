from dotenv import load_dotenv
import os
import discord

from discord.ext import commands

# cogs
from cors.cogChattings import CogChattings
from cors.cogRant import CogRant

# data
from data.dataRant import DataRant

load_dotenv()

# Membuat object Intents
intents = discord.Intents.default()
intents.message_content = True

# prefix commadn di awali dengan '!'
bot = commands.Bot(command_prefix="!", intents=intents)
# help_command=None )  # commadn default

# other config

# @bot.command(name="helpChat")
# async def helpChat(ctx: commands.Context):
#     user = ctx.author
#     await ctx.send(f" thank for chat {user}")
#     await ctx.send("Help command")


dataRant = DataRant()


@bot.event
async def on_ready():
    print("Bot online")
    await bot.change_presence(activity=discord.Game(name="!help"))


@bot.command(name="info")
async def info(ctx: commands.Context):
    await ctx.send("Rant Bot ")
    await ctx.send("Jaga sopan santunya ya")


# cog atau kelompok Mesage Bot
bot.add_cog(CogChattings(bot))
bot.add_cog(CogRant(bot=bot, dataRant=dataRant))


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    print("Bot online")
    bot.run(token)
