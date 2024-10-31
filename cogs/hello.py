
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Say hello."""
        if "hello" in message.content.lower():
            self.bot.log(f"hello {message.author.name}, got your message {message.content}", "purple")

async def setup(bot):
    await bot.add_cog(Hello(bot))