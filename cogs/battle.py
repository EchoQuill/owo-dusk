import asyncio
import json

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

cmd = {
    "cmd_name": "battle",
    "prefix": True,
    "checks": True,
    "retry_count": 0
}

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - Battle","purple")
    
    async def cog_load(self):
        if not config_dict["commands"]["battle"]["enabled"]:
            try:
                await self.bot.unload_extension("cogs.battle")
            except:
                pass
        self.bot.put_queue(cmd)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if message.embeds:
                for embed in message.embeds:
                    if embed.author.name is not None and "goes into battle!" in embed.author.name.lower():
                        self.bot.remove_queue(cmd)
                        self.bot.log(f"Removed battle from checks from main","cornflower_blue")
                        await asyncio.sleep(self.bot.random_float(config_dict["commands"]["hunt"]["cooldown"]))
                        """
                        self.bot.checks.remove((command, timestamp))
                        is not used to prevent valueerror and better error management
                        """
                        self.bot.put_queue(cmd)
                        self.bot.log(f"Added battle to queue again from main","cornflower_blue")
                
                


async def setup(bot):
    await bot.add_cog(Battle(bot))