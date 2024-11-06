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
    
    async def cog_load(self):
        if not config_dict["commands"]["battle"]["enabled"]:
            await self.bot.unload_extension("cogs.giveaway")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if message.embeds:
                for embed in message.embeds:
                    if embed.author.name is not None and "goes into battle!" in embed.author.name.lower():
                        await asyncio.sleep(self.bot.random_float(config_dict["commands"]["hunt"]["cooldown"]))
                        self.bot.queue.put("battle")
                
                


async def setup(bot):
    await bot.add_cog(Owo(bot))