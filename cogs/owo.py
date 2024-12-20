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
    "cmd_name": "owo",
    "prefix": False,
    "checks": True,
    "retry_count": 0
}

class Owo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - OwO","purple")
    
    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if not config_dict["commands"]["owo"]["enabled"]:
            try:
                await self.bot.unload_extension("cogs.owo")
            except ExtensionNotLoaded:
                pass
        else:
            self.bot.put_queue(cmd)
        
            

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.user.id:
            if "owo" == message.content:
                self.bot.log(f"owo detected from {message.author.name}.","cornflower_blue")
                self.bot.remove_queue(cmd)
                await asyncio.sleep(self.bot.random_float(config_dict["commands"]["owo"]["cooldown"]))
                #self.bot.queue.put(["owo", [True, True]])
                self.bot.put_queue(cmd)
                self.bot.log(f"owo put to queue again","cornflower_blue")
                
                


async def setup(bot):
    await bot.add_cog(Owo(bot))