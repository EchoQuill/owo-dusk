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
import re

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded

cash_regex = r"for \*\*(\d+)\*\* <:cowoncy:\d+>"

cash_required = {
    1:10,
    2:100,
    3:1000,
    4:10000,
    5:100000,
    6:1000000,
    7:10000000
}

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {
            "cmd_name": "buy",
            "cmd_arguments": "",
            "prefix": True,
            "checks": True,
            "retry_count": 0,
            "id": "shop"
        }

    async def cog_load(self):
        if not self.bot.config_dict["commands"]["shop"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.shop"))
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.send_buy(startup=True))

    async def cog_unload(self):
        await self.bot.remove_queue(id="shop")

    async def send_buy(self, startup=False):
        item = random.choice(self.bot.config_dict["commands"]["shop"]["itemsToBuy"])
        if startup:
            await self.bot.sleep_till(self.bot.config_dict["defaultCooldowns"]["shortCooldown"])
        else:
            await self.bot.remove_queue(id="shop")
            await self.bot.sleep_till(self.bot.config_dict["commands"]["shop"]["cooldown"])
        if cash_required[item] <= self.bot.balance:
            self.cmd["cmd_arguments"] = item
            await self.bot.put_queue(self.cmd)
        else:
            await self.send_buy()


    @commands.Cog.listener()
    async def on_message(self, message):
        """
        🛒 **| user**, you bought a <:cring:590393333331918859> **Common Ring** for **10** <:cowoncy:416043450337853441>!
        """
        if "**, you bought a " in message.content:
            print(message.content)
            self.bot.balance-=int(re.search(cash_regex, message.content).group(1))
            await self.send_buy()


async def setup(bot):
    await bot.add_cog(Shop(bot))
