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


class Pray(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - Pray/Curse","purple")
        self.pray_cmd_arguement = None
        self.curse_cmd_arguement = None
        self.pray_cmd = {
            "cmd_name": "pray",
            "cmd_arguments": None,
            "prefix": True,
            "checks": True,
            "retry_count": 0
        }

        self.curse_cmd = {
            "cmd_name": "curse",
            "cmd_arguments": None,
            "prefix": True,
            "checks": True,
            "retry_count": 0
        }

    async def startup(self):
        await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["shortCooldown"]))
        self.start_pray_curse()

    async def start_pray_curse(self, cmd=None):
        """
        this long messed up code is temporary, but hey atleast it still works

        issues:-
        using similar code twice
        startup has higher delay than required

        """
        if config_dict["commands"]["pray"]["enabled"]:
            self.bot.remove_queue(self.pray_cmd)
            self.bot.log(f"Removed pray from checks from main","cornflower_blue")
            await asyncio.sleep(self.bot.random_float(config_dict["commands"]["curse"]["cooldown"]))
            self.pray_cmd_arguement = cmd_argument(config_dict['commands']['pray']['userid'], config_dict['commands']['pray']['pingUser'])
            self.pray_cmd["cmd_arguments"]=self.pray_cmd_arguement
            self.bot.state = False
            await self.bot.put_queue(self.pray_cmd)
        else:
            self.bot.remove_queue(self.curse_cmd)
            self.bot.log(f"Removed curse from checks from main","cornflower_blue")
            await asyncio.sleep(self.bot.random_float(config_dict["commands"]["curse"]["cooldown"]))
            self.curse_cmd_arguement = cmd_argument(config_dict['commands']['curse']['userid'], config_dict['commands']['curse']['pingUser'])
            self.curse_cmd["cmd_arguments"]=self.curse_cmd_arguement
            self.bot.state = False
            await self.bot.put_queue(self.curse_cmd)

    async def cog_load(self):
        try:
            if not config_dict["commands"]["pray"]["enabled"] and not config_dict["commands"]["curse"]["enabled"]:
                try:
                    await self.bot.unload_extension("cogs.pray")
                except ExtensionNotLoaded:
                    pass
            else:
                asyncio.create_task(self.start_pray_curse())
        except Exception as e:
            print(e)
    


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            """ add individual ones as well """

            """
            **⏱ | user**! Slow down and try the command again **<t:1734943219:R>**
            """

            """pray"""
            if ((f"<@{self.bot.user.id}>** prays for **<@{config_dict['commands']['pray']['userid']}>**!" in message.content
            or f"<@{self.bot.user.id}** prays..." in message.content
            or "Slow down and try the command again" in message.content) and
            config_dict['commands']['pray']['enabled']):
                self.start_pray_curse("pray")
            """curse"""
            if ((f"<@{self.bot.user.id}>** puts a curse on **<@{config_dict['commands']['curse']['userid']}>**!" in message.content
            or f"<@{self.bot.user.id}>** is now cursed." in message.content 
            or "Slow down and try the command again" in message.content) and
            config_dict['commands']['curse']['enabled']):
                self.start_pray_curse("curse")
                
                
                


async def setup(bot):
    await bot.add_cog(Pray(bot))
