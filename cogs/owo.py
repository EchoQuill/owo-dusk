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


class Owo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owo_ongoing = False

    async def send_owo(self, startup=False):
        if not self.bot.captcha and self.bot.state:
            if not startup:
                self.owo_ongoing = True
                await self.bot.sleep_till(self.bot.config_dict["commands"]["owo"]["cooldown"])
                self.owo_ongoing = False
            await self.bot.upd_cmd_state("owo")
            await self.bot.send(self.bot.alias["owo"]["normal"])
            
    
    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if not self.bot.config_dict["commands"]["owo"]["enabled"] or self.bot.config_dict["defaultCooldowns"]["reactionBot"]["owo"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.owo"))
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.send_owo(startup=True))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.user.id:
            if message.content in {'owo', 'uwu'}:
                if not self.owo_ongoing:
                    await self.send_owo()




async def setup(bot):
    await bot.add_cog(Owo(bot))