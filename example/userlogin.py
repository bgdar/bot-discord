
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Contoh ID server dan ID user dari database website
GUILD_ID = 123456789012345678
DISCORD_USER_ID_DARI_WEB = 987654321098765432


# *Bgdar : datanya di kirm viw RabbitMq nantik , ok
@bot.event
async def on_ready():
    print(f"Bot {bot.user} siap!")

    # 1. Ambil objek server
    guild = bot.get_guild(GUILD_ID)
    if guild:
        # 2. Cek apakah user ada di server tersebut
        member = guild.get_member(DISCORD_USER_ID_DARI_WEB)
        # *Bgdar : nantik atur role bagi user , dna pada role yang belum login tidakk bisa melakukna chatting dan sebagainay

        if member:
            print(
                f"User {member.name} terverifikasi ada di dalam server Discord.")
            # Di sini Anda bisa memberikan role otomatis jika mau
            # await member.add_roles(role_terverifikasi)
        else:
            print("User terdaftar di web, tetapi belum masuk ke server Discord.")
