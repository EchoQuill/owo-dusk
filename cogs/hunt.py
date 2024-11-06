import asyncio
import random
import json

from discord.ext import commands

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

class Owo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - OwO","purple")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if 'you found:' in message.content.lower() or "caught" in message.content.lower():
                await asyncio.sleep(self.bot.random_float(config_dict["commands"]["hunt"]["cooldown"]))
                self.bot.queue.put("hunt")
                
                
                


async def setup(bot):
    await bot.add_cog(Owo(bot))