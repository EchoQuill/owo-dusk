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

"""sell_rarity = ""
for i in config_dict["commands"]["sell"]["rarity"]:
    sell_rarity+=f"{i} "
else:
    #else runs always since `break` is not used
    sell_rarity = sell_rarity[:-1]"""
sell_rarity = " ".join(config_dict["commands"]["sell"]["rarity"])
sac_rarity = " ".join(config_dict["commands"]["sac"]["rarity"])


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
            self.bot.queue.put(["sell", f" {sell_rarity}"])
        else:
            await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sac"]["cooldown"]))
            self.bot.queue.put(["sac", f" {sac_rarity}"])
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if 'for a total of **<:cowoncy:416043450337853441>' in message.content.lower():
                self.bot.checks = [check for check in self.bot.checks if check[0] != "sell"]
                try:
                    self.bot.balance += int(re.search(r'for a total of \*\*<:cowoncy:\d+> ([\d,]+)', message.content).group(1).replace(',', ''))
                except:
                    self.bot.log(f"{self.bot.user}[+] failed to fetch cowoncy from sales,", "cyan3")
                if config_dict["commands"]["sac"]["enabled"]:
                    await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sac"]["cooldown"]))
                    self.bot.queue.put(["sac", f" {sac_rarity}"])
                else:
                    await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sell"]["cooldown"]))
                    self.bot.queue.put(["sell", f" {sell_rarity}"])

            elif "sacrificed" in message.content and "for a total of" in message.content.lower():
                self.bot.checks = [check for check in self.bot.checks if check[0] != "sac"]
                if config_dict["commands"]["sell"]["enabled"]:
                    await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sell"]["cooldown"]))
                    self.bot.queue.put(["sell", f" {sell_rarity}"])
                else:
                    await asyncio.sleep(self.bot.random_float(config_dict["commands"]["sac"]["cooldown"]))
                    self.bot.queue.put(["sac", f" {sac_rarity}"])


async def setup(bot):
    await bot.add_cog(Sell(bot))