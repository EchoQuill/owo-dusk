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
import random

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

def cmd_argument(userid, ping):
    if userid:
        return f"<@{random.choice(userid)}>" if ping else random.choice(userid)
    else:
        return ""

pray_cmd = {
    "cmd_name": "pray",
    "cmd_arguments": cmd_argument(config_dict['commands']['pray']['userid'], config_dict['commands']['pray']['pingUser']),
    "prefix": True,
    "checks": True,
    "retry_count": 0
}

curse_cmd = {
    "cmd_name": "curse",
    "cmd_arguments": cmd_argument(config_dict['commands']['curse']['userid'], config_dict['commands']['curse']['pingUser']),
    "prefix": True,
    "checks": True,
    "retry_count": 0
}

class Pray(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - Pray/Curse","purple")

    async def cog_load(self):
        if not config_dict["commands"]["pray"]["enabled"] and not config_dict["commands"]["curse"]["enabled"]:
            try:
                await self.bot.unload_extension("cogs.pray")
            except ExtensionNotLoaded:
                pass
        else:
            if config_dict["commands"]["pray"]["enabled"]:
                await self.bot.put_queue(pray_cmd)
            else:
                await self.bot.put_queue(curse_cmd)
    


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            """ add individual ones as well """
            """pray"""
            if (f"<@{self.bot.user.id}>** prays for **<@{config_dict['commands']['pray']['userid']}>**!"
            or f"<@{self.bot.user.id}** prays... Luck is on your side!" in message.content):
                self.bot.remove_queue(pray_cmd)
                self.bot.log(f"Removed pray from checks from main","cornflower_blue")
                await asyncio.sleep(self.bot.random_float(config_dict["commands"]["pray"]["cooldown"]))
                await self.bot.put_queue(pray_cmd)
                self.bot.log(f"Added pray to queue again from main","cornflower_blue")
            """curse"""
            if (f"<@{self.bot.user.id}>** puts a curse on **<@{config_dict['commands']['curse']['userid']}>**!" in message.content
            or 
            f"<@{self.bot.user.id}>** is now cursed." in message.content):
                self.bot.remove_queue(pray_cmd)
                self.bot.log(f"Removed pray from checks from main","cornflower_blue")
                await asyncio.sleep(self.bot.random_float(config_dict["commands"]["pray"]["cooldown"]))
                await self.bot.put_queue(pray_cmd)
                self.bot.log(f"Added pray to queue again from main","cornflower_blue")
                
                
                


async def setup(bot):
    await bot.add_cog(Pray(bot))
