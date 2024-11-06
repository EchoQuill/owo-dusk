import asyncio
import json

from discord.ext import commands

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

class Owo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - OwO","purple")
    
    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if not config_dict["commands"]["owo"]["enabled"]:
            await self.bot.unload_extension("cogs.giveaway")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.user.id:
            if "owo" in message.content.lower():
                await asyncio.sleep(self.bot.random_float(config_dict["commands"]["owo"]["cooldown"]))
                self.bot.queue.put("owo")
                
                


async def setup(bot):
    await bot.add_cog(Owo(bot))