from discord.ext import commands
import discord
from data.dataRant import DataRant


class CogRant(commands.Cog):
    """Deteksi Kata kata kasar"""

    def __init__(self, bot: commands.Bot, dataRant: DataRant):
        self.bot = bot
        self.dataRant = dataRant

    @commands.command(name="kataList")
    async def kataList(self, ctx: commands.Context):
        """list kata kata kasar : !kataList"""
        kata = self.dataRant.allWords
        await ctx.send(f"Kata kasar {kata}")

    @commands.command("newWord")
    async def newWord(self, ctx: commands.Context, *args):
        """beri tau bot kata kata yang kasar"""
        if ctx.bot:
            return

        if len(args) == 0:
            await ctx.send(
                "maksudnya !!! , seperti ini !newWord <kata>,<kategori>,<level> ya "
            )
            return
        words = args.split(",")
        kata = words[0]
        kateori = words[1] if len(words) >= 2 else "uknown"
        level = words[2] if len(words) >= 3 else "normal"
        self.dataRant.addNewWord(kata, kateori, level)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Listener untuk mendeteksi kata kasar secara efisien"""
        if message.author.bot:  # jika yg kirim bot ya gak ada kata kasar
            return

        # Pecah kata dalam message → set untuk O(1) lookup
        user_words = set(message.content.lower().split())

        # Cek intersection dengan kata kasar , dari allWord
        # intersections : untuk membandingkan dan menghasilkan set baru dengan isi kata kasar
        detected_words = user_words.intersection(self.dataRant.allWords)
        print("detected word :", detected_words)

        if detected_words:
            responses = []
            for word in detected_words:
                name, level = self.dataRant.getRantInfo(word)
                responses.append(f"- `{word}` → kategori: {name}, level: {level}")

            await message.channel.send(
                f"Hey {message.author}, jangan pakai kata kasar! Deteksi:\n"
                + "\n".join(responses)
            )

            # Hapus message setelah 15 detik
            await message.delete(delay=15)

        # lanjutkan ke command lain
        await self.bot.process_commands(message)
