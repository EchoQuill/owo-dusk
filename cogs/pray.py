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
import random

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded


def cmd_argument(userid, ping):
    if userid:
        return f"<@{random.choice(userid)}>" if ping else random.choice(userid)
    else:
        return ""


class Pray(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pray_cmd_arguement = None
        self.curse_cmd_arguement = None
        self.startup = True
        self.pray_cmd = {
            "cmd_name": "pray",
            "cmd_arguments": None,
            "prefix": True,
            "checks": True,
            "retry_count": 2,
            "id": "pray"
        }

        self.curse_cmd = {
            "cmd_name": "curse",
            "cmd_arguments": None,
            "prefix": True,
            "checks": True,
            "retry_count": 2,
            "id": "pray" # using pray as id for curse to make it easier to close
        }
        self.cmd_names = []

    async def start_pray_curse(self):
        cmds = [cmd for cmd in ["pray", "curse"] if self.bot.config_dict['commands'][cmd]['enabled']]
        cmd = random.choice(cmds) # pick a random enabled cmd
        if not self.startup:
            await self.bot.remove_queue(id="pray")
            await self.bot.log("removed pray from queue", "#d0ff78")
            await self.bot.sleep_till(self.bot.config_dict["commands"][cmd]["cooldown"])
            self.__dict__[f"{cmd}_cmd"]["checks"] = True
        else:
            await self.bot.sleep_till(self.bot.config_dict["defaultCooldowns"]["shortCooldown"])
            self.__dict__[f"{cmd}_cmd"]["checks"] = False

        cmd_argument_data = cmd_argument(
            self.bot.config_dict['commands'][cmd]['userid'], self.bot.config_dict['commands'][cmd]['pingUser']
        )

        self.__dict__[f"{cmd}_cmd"]["cmd_arguments"] = cmd_argument_data
        await self.bot.put_queue(self.__dict__[f"{cmd}_cmd"], priority=True)
        await self.bot.log("added pray to queue", "#d0ff78")
        if self.startup:
            """
            Sometimes the pray/curse may have already ran twice within 5 mins after a successful run
            before owo-dusk is ran, this check is to fix it getting the code stuck.
            """
            await self.bot.sleep_till(self.bot.config_dict["defaultCooldowns"]["shortCooldown"])
            if self.startup:
                self.startup=False
                await self.start_pray_curse()

    async def cog_load(self):
        try:
            if not self.bot.config_dict["commands"]["pray"]["enabled"] and not self.bot.config_dict["commands"]["curse"]["enabled"]:
                try:
                    asyncio.create_task(self.bot.unload_cog("cogs.pray"))
                except ExtensionNotLoaded:
                    pass
            else:
                asyncio.create_task(self.start_pray_curse())
        except Exception as e:
            print(e)

    async def cog_unload(self):
        await self.bot.remove_queue(id="pray")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            """
            **⏱ | user**! Slow down and try the command again **<t:1734943219:R>**
            """

            if (
                f"<@{self.bot.user.id}>** prays for **<@{self.bot.config_dict['commands']['pray']['userid']}>**!"
                in message.content
                or f"<@{self.bot.user.id}>** prays..." in message.content
                or f"<@{self.bot.user.id}>** puts a curse on **<@{self.bot.config_dict['commands']['curse']['userid']}>**!"
                in message.content
                or f"<@{self.bot.user.id}>** is now cursed." in message.content
                #or "Slow down and try the command again" in message.content
            ):
                await self.bot.log("prayed successfully!", "#d0ff78")
                self.startup = False
                await self.start_pray_curse()


async def setup(bot):
    await bot.add_cog(Pray(bot))
