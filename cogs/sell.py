import json
import re
import asyncio

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded

"""
TASK:
improve cooldown system (somehow) to make both same.
perhaps make a new category `animals` as we are already handling command being put seperately...?
"""

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

class Sell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - sell","purple")

    async def cog_load(self):
        if not config_dict["commands"]["sell"]["enabled"] and not config_dict["commands"]["sac"]["enabled"]:
            try:
                await self.bot.unload_extension("cogs.sell")
            except ExtensionNotLoaded:
                pass
        if (config_dict["commands"]["sell"]["enabled"] and config_dict["commands"]["sac"]["enabled"]) or (config_dict["commands"]["sell"]["enabled"]):
            # start sell first.
            await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sell"]["cooldown"]))
            self.bot.queue.put("sell")
        else:
            await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sac"]["cooldown"]))
            self.bot.queue.put("sac")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if 'for a total of **<:cowoncy:416043450337853441>' in message.content.lower():
                try:
                    self.bot.balance += int(re.search(r'for a total of \*\*<:cowoncy:\d+> ([\d,]+)', message.content).group(1).replace(',', ''))
                except:
                    self.bot.log(f"{self.bot.user}[+] failed to fetch cowoncy from sales,", "cyan3")
                if config_dict["commands"]["sac"]["enabled"]:
                    await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sac"]["cooldown"]))
                    self.bot.queue.put("sac")
                else:
                    await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sell"]["cooldown"]))
                    self.bot.queue.put("sell")

            elif "sacrificed" in message.content and "for a total of" in message.content.lower():
                if config_dict["commands"]["sell"]["enabled"]:
                    await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sell"]["cooldown"]))
                    self.bot.queue.put("sell")
                else:
                    await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sac"]["cooldown"]))
                    self.bot.queue.put("sac")

                
                


async def setup(bot):
    await bot.add_cog(Sell(bot))