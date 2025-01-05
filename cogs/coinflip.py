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

import re
import json
import asyncio
import random

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded


won_pattern = r"you won \*\*<:cowoncy:\d+> ([\d,]+)"


class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {
            "cmd_name": "coinflip",
            "cmd_arguments": None,
            "prefix": True,
            "checks": True,
            "retry_count": 0,
            "id": "coinflip"
        }
        self.turns_lost = 0


    async def cog_load(self):
        if not self.bot.config_dict["gamble"]["coinflip"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.coinflip"))
            except ExtensionNotLoaded as e:
                print(e)
            except Exception as e:
                print(e)
        else:
            asyncio.create_task(self.start_cf(startup=True))
            
    async def cog_unload(self):
        await self.bot.remove_queue(id="coinflip")

    async def start_cf(self, startup=False):
        try:
            if startup:
                await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["shortCooldown"]))
            else:
                await asyncio.sleep(self.bot.random_float(self.bot.config_dict["gamble"]["coinflip"]["cooldown"]))
            

            self.cmd["cmd_arguments"] = str(self.bot.config_dict["gamble"]["coinflip"]["startValue"]*(self.bot.config_dict["gamble"]["coinflip"]["multiplierOnLose"]**self.turns_lost))
            if self.bot.config_dict["gamble"]["coinflip"]["options"]:
                self.cmd["cmd_arguments"]+=f" {random.choice(self.bot.config_dict["gamble"]["coinflip"]["options"])}"
            await self.bot.put_queue(self.cmd)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != 408785106942164992:
            return
        if message.channel.id != self.bot.channel_id:
            return
        
        if "and chose" in message.content:
            await self.bot.remove_queue(self.cmd)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.id != 408785106942164992:
            return
        if before.channel.id != self.bot.channel_id:
            return
        
        if "chose" in after.content.lower():
            try:
                if "and you lost it all... :c" in after.content.lower():
                    self.turns_lost+=1
                    await self.start_cf()
                else:
                    try:
                        match = int(re.search(won_pattern, after.content).group(1).replace(",",""))
                    except Exception as e:
                        print(e)
                    self.turns_lost = 0
                    await self.start_cf()
                    self.bot.balance+=int(match)
            except Exception as e:
                print(e)

async def setup(bot):
    await bot.add_cog(Coinflip(bot))

