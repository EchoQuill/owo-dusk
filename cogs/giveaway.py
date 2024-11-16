import asyncio
import json

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2","purple")

    """Join previous giveaways"""
    async def join_previous_giveaways(self):
        self.bot.log(f"{self.bot.user}[+] waiting~~", "cyan3")
        await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["shortCooldown"]))
        self.bot.log(f"{self.bot.user}[+] started~~", "cyan3")
        self.bot.log(f"conf","purple")
        self.bot.state = False
        # Using briefcooldown here as using the long cooldown of giveaway joiner might look weird here.
        await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["briefCooldown"]))
        for i in config_dict["giveawayJoiner"]["channelsToJoin"]:
            channel = self.bot.get_channel(i)
            if not channel:
                # To prevent giving error if channel id is invalid
                continue
            async for message in channel.history(limit=6):
                if message.embeds:
                    for embed in message.embeds:
                        if embed.author.name is not None and " A New Giveaway Appeared!" in embed.author.name and message.channel.id in config_dict["giveawayJoiner"]["channelsToJoin"]:
                            await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["briefCooldown"]))
                            if message.components[0].children[0] and not message.components[0].children[0].disabled:
                                await message.components[0].children[0].click()
                                self.bot.log(f"{self.bot.user}[+] giveaway joined in {message.channel.name}", "cyan3")

        self.bot.state = True

    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if config_dict["giveawayJoiner"]["enabled"]:
            """Run join_previous_giveaways when bot is ready"""
            asyncio.create_task(self.join_previous_giveaways())
        else:
            try:
                await self.bot.unload_extension("cogs.giveaway")
            except ExtensionNotLoaded:
                pass
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Join Giveaways"""
        if message.channel.id in config_dict["giveawayJoiner"]["channelsToJoin"]:
            if message.embeds:
                for embed in message.embeds:
                    if embed.author.name is not None and " A New Giveaway Appeared!" in embed.author.name and message.channel.id in config_dict["giveawayJoiner"]["channelsToJoin"]:
                        await asyncio.sleep(self.bot.random_float(config_dict["giveawayJoiner"]["cooldown"]))
                        if message.components[0].children[0] and not message.components[0].children[0].disabled:
                            await message.components[0].children[0].click()
                            self.bot.log(f"{self.bot.user}[+] giveaway joined in {message.channel.name}", "cyan3")

async def setup(bot):
    await bot.add_cog(Giveaway(bot))