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

import json
import re
import asyncio

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded

"""
TASK:
improve cooldown system (somehow) to make both same.
perhaps make a new category `animals` as we are already handling command being put seperately...?
"""





class Sell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sell_cmd = {
            "cmd_name": "sell",
            "cmd_arguments": " ".join(self.bot.config_dict["commands"]["sell"]["rarity"]),
            "prefix": True,
            "checks": True,
            "retry_count": 0,
            "id": "sell"
        }

        self.sac_cmd = {
            "cmd_name": "sac",
            "cmd_arguments": " ".join(self.bot.config_dict["commands"]["sac"]["rarity"]),
            "prefix": True,
            "checks": True,
            "retry_count": 0,
            "id": "sell"
        }

    async def sell_sac_queue(self, cmd, cooldown):
        await asyncio.sleep(self.bot.random_float(cooldown))
        #self.bot.queue.put(["sell", f" {sell_rarity if cmd=="sell" else sac_rarity}"])
        #self.bot.put_queue(f"sell {sell_rarity if cmd=="sell" else sac_rarity}")
        await self.bot.put_queue(cmd)



    async def cog_load(self):
        if not self.bot.config_dict["commands"]["sell"]["enabled"] and not self.bot.config_dict["commands"]["sac"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.sell"))
            except ExtensionNotLoaded:
                pass
        else:
            if (self.bot.config_dict["commands"]["sell"]["enabled"] and self.bot.config_dict["commands"]["sac"]["enabled"]) or (self.bot.config_dict["commands"]["sell"]["enabled"]):
                # start sell first.
                asyncio.create_task(self.sell_sac_queue(self.sell_cmd, self.bot.config_dict["commands"]["sell"]["cooldown"]))
            else:
                asyncio.create_task(self.sell_sac_queue(self.sac_cmd, self.bot.config_dict["commands"]["sac"]["cooldown"]))

    async def cog_unload(self):
        self.bot.remove_queue(id="sell")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if 'for a total of **<:cowoncy:416043450337853441>' in message.content.lower():
                self.bot.remove_queue(self.self.sell_cmd)

                try:
                    self.bot.balance += int(re.search(r'for a total of \*\*<:cowoncy:\d+> ([\d,]+)', message.content).group(1).replace(',', ''))
                except:
                    self.bot.log(f"{self.bot.user}[+] failed to fetch cowoncy from sales,", "cyan3")
                if self.bot.config_dict["commands"]["sac"]["enabled"]:
                    await self.sell_sac_queue(self.sac_cmd, self.bot.config_dict["commands"]["sac"]["cooldown"])
                else:
                    await self.sell_sac_queue(self.sell_cmd, self.bot.config_dict["commands"]["sell"]["cooldown"])

            elif "sacrificed" in message.content and "for a total of" in message.content.lower():
                self.bot.remove_queue(self.sac_cmd)
                if self.bot.config_dict["commands"]["sell"]["enabled"]:
                    await self.sell_sac_queue(self.sell_cmd, self.bot.config_dict["commands"]["sell"]["cooldown"])
                else:
                    await self.sell_sac_queue(self.sac_cmd, self.bot.config_dict["commands"]["sac"]["cooldown"])


async def setup(bot):
    await bot.add_cog(Sell(bot))