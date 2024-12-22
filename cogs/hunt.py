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

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

cmd = {
    "cmd_name": "hunt",
    "prefix": True,
    "checks": True,
    "retry_count": 0
}

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
        else:
            await self.bot.put_queue(cmd)
    


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if 'you found:' in message.content.lower() or "caught" in message.content.lower():
                self.bot.remove_queue(cmd)
                self.bot.log(f"Removed hunt from checks from main","cornflower_blue")
                await asyncio.sleep(self.bot.random_float(config_dict["commands"]["hunt"]["cooldown"]))
                await self.bot.put_queue(cmd)
                self.bot.log(f"Added Hunt to queue again from main","cornflower_blue")
                
                
                


async def setup(bot):
    await bot.add_cog(Hunt(bot))
