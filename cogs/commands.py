
import asyncio
import random
import json
import queue

from discord.ext import commands, tasks

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - commands","purple")
        self.bot.checks = []

    async def cog_load(self):
        """Run join_previous_giveaways when bot is ready"""
        self.bot.log(f"{self.bot.user}[+] waiting~~", "cyan3")
        await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["briefCooldown"]))
        self.send_commands.start()
        self.bot.log(f"{self.bot.user}[+] started sending commands~~", "cyan3")

    """send commands"""
    @tasks.loop()
    async def send_commands(self):
        """
        This may need a bit improvement as
        it just looks bad to me for some reason haha
        """
        for i in self.bot.queue:
            if self.bot.state and not self.bot.captcha:
                if i == "lvlGrind":
                    continue
                elif i == "shop":
                    await self.bot.send(f"buy {random.choice(config_dict["commands"]["shop"]["itemsToBuy"])}")
                elif i == "autoHuntBot":
                    continue
                elif i == "owo":
                    await self.bot.send(i, noprefix=True)
                else:
                    await self.bot.send(i)




async def setup(bot):
    await bot.add_cog(Commands(bot))