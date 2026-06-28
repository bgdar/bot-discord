from dotenv import load_dotenv
import os
import discord

from discord.ext import commands

# cogs
from cors.cogChattings import CogUser
from cors.cogRant import CogRant

from service import helpInfo

# data
# Bgdar : gak pakek lagi , sekarang mengguanak service App terpisah
# from dataJson.dataRant import DataRant

load_dotenv()

# Membuat object Intents
intents = discord.Intents.default()
intents.message_content = True

# prefix commadn di awali dengan '!'
bot = commands.Bot(command_prefix="!", intents=intents)
# help_command=None )  # commadn default biarkan aktive

# other config

# @bot.command(name="helpChat")
# async def helpChat(ctx: commands.Context):
#     user = ctx.author
#     await ctx.send(f" thank for chat {user}")
#     await ctx.send("Help command")


# dataRant = DataRant()


@bot.event
async def on_ready():
    print("Bot online")
    await bot.change_presence(activity=discord.Game(name="!help"))


@bot.command(name="info",)
async def info(ctx: commands.Context):
    helpInfo(ctx)
# akan di awali dengan "/"


@bot.slash_command(name="info", description="Infomasi tentang rant Bot")
async def info(ctx: commands.Context):
    helpInfo(ctx)


# cog atau kelompok Mesage Bot
bot.add_cog(CogUser(bot))
# bot.add_cog(CogRant(bot=bot, dataRant=dataRant))
bot.add_cog(CogRant(bot=bot))


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    print("Bot online")
    bot.run(token)
