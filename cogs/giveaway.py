# This file is part of owo-dusk.
#
# Copyright (c) 2024-present EchoQuill
#
# Portions of this file are based on code by EchoQuill, licensed under the
# GNU General Public License v3.0 (GPL-3.0).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import asyncio

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded



class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Join previous giveaways"""
    async def join_previous_giveaways(self):
        await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["shortCooldown"])
        await self.bot.wait_until_ready()
        
        # Using briefcooldown here as using the long cooldown of giveaway joiner might look weird here.
        await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["briefCooldown"])
        for i in self.bot.settings_dict["giveawayJoiner"]["channelsToJoin"]:
            try:
                channel = await self.bot.fetch_channel(i)
            except:
                channel = None
            if not channel:
                # To prevent giving error if channel id is invalid
                await self.bot.log(f"giveaway channel seems to be invalid", "#ff5f00")
                continue
            await self.bot.set_stat(False)
            async for message in channel.history(limit=self.bot.settings_dict["giveawayJoiner"]["messageRangeToCheck"]):
                if message.embeds:
                    for embed in message.embeds:
                        if embed.author.name is not None and " A New Giveaway Appeared!" in embed.author.name and message.channel.id in self.bot.settings_dict["giveawayJoiner"]["channelsToJoin"]:
                            await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["briefCooldown"])
                            if message.components[0].children[0] and not message.components[0].children[0].disabled:
                                await message.components[0].children[0].click()
                                await self.bot.log(f"giveaway joined in {message.channel.name}", "#00d7af")

            await self.bot.set_stat(True)

    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if self.bot.settings_dict["giveawayJoiner"]["enabled"]:
            """Run join_previous_giveaways when bot is ready"""
            asyncio.create_task(self.join_previous_giveaways())
        else:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.giveaway"))
            except ExtensionNotLoaded:
                pass
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Join Giveaways"""
        if message.channel.id in self.bot.settings_dict["giveawayJoiner"]["channelsToJoin"]:
            if message.embeds:
                for embed in message.embeds:
                    if embed.author.name is not None and " A New Giveaway Appeared!" in embed.author.name and message.channel.id in self.bot.settings_dict["giveawayJoiner"]["channelsToJoin"]:
                        await self.bot.sleep_till(self.bot.settings_dict["giveawayJoiner"]["cooldown"])
                        if message.components[0].children[0] and not message.components[0].children[0].disabled:
                            await message.components[0].children[0].click()

async def setup(bot):
    await bot.add_cog(Giveaway(bot))