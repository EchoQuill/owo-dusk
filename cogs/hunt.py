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
import json

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded




class Hunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {
            "cmd_name": "h" if self.bot.config_dict["commands"]["hunt"]["useShortForm"] else "hunt",
            "prefix": True,
            "checks": True,
            "retry_count": 0
        }

    async def cog_load(self):
        if not self.bot.config_dict["commands"]["hunt"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.hunt"))
            except ExtensionNotLoaded:
                pass
        else:
            await self.bot.put_queue(self.cmd)
            self.bot.log(f"Added Hunt to queue again from main","cornflower_blue")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
                if 'you found:' in message.content.lower() or "caught" in message.content.lower():
                    self.bot.remove_queue(self.cmd)
                    self.bot.log(f"Removed hunt from checks from main","cornflower_blue")
                    await asyncio.sleep(self.bot.random_float(self.bot.config_dict["commands"]["hunt"]["cooldown"]))
                    await self.bot.put_queue(self.cmd)
                    self.bot.log(f"Added Hunt to queue again from main","cornflower_blue")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Hunt(bot))
