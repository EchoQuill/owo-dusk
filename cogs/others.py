import asyncio
import random
import json

from discord.ext import commands

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

class Others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - others","purple")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if "**you must accept these rules to use the bot!**" in message.content.lower():
                await asyncio.sleep(random.uniform(0.6,1.7))
                if message.components[0].children[0] and not message.components[0].children[0].disabled:
                    await message.components[0].children[0].click()
                self.bot.log(f"-{self.user}[+] Accepted OwO bot rules","spring_green1")

async def setup(bot):
    await bot.add_cog(Others(bot))