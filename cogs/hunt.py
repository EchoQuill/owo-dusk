import asyncio
import json

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

class Hunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - Hunt","purple")

    async def cog_load(self):
        if not config_dict["commands"]["hunt"]["enabled"]:
            try:
                await self.bot.unload_extension("cogs.hunt")
            except ExtensionNotLoaded:
                pass
    


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if 'you found:' in message.content.lower() or "caught" in message.content.lower():
                self.bot.checks = [check for check in self.bot.checks if check[0] != "hunt"]
                self.bot.log(f"Removed hunt from checks from main","cornflower_blue")
                await asyncio.sleep(self.bot.random_float(config_dict["commands"]["hunt"]["cooldown"]))
                self.bot.put_queue("hunt")
                self.bot.log(f"Added Hunt to queue again from main","cornflower_blue")
                
                
                


async def setup(bot):
    await bot.add_cog(Hunt(bot))
