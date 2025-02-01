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

from discord.ext import commands, tasks
from discord.ext.commands import ExtensionNotLoaded


class Owo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.cmd = {
            "cmd_name": self.bot.alias["owo"]["normal"],
            "prefix": False,
            "checks": False,
            "retry_count": 0,
            "id": "owo"
        }

    @tasks.loop(seconds=1)
    async def send_owo(self):
        if not self.bot.captcha and self.bot.state:
            await asyncio.sleep(self.bot.random_float(self.bot.config_dict["commands"]["owo"]["cooldown"]))
            await self.bot.put_queue(self.cmd)
    
    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if not self.bot.config_dict["commands"]["owo"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.owo"))
            except ExtensionNotLoaded:
                pass
        else:
            self.send_owo.start()

    async def cog_unload(self):
        self.send_owo.stop()


async def setup(bot):
    await bot.add_cog(Owo(bot))