

from discord.ext import commands

class Bye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Say hello."""
        if "bye" in message.content.lower():
            print("woah bye!")

async def setup(bot):
    await bot.add_cog(Bye(bot))
