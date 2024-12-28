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


"""
Ok so technically,
2*2 =4 = 2*(2)
4*2 = 8 = 2*(2*2)
8*2 = 16 = 2*(2*2*2)
"""

won_pattern = r"and won <:cowoncy:\d+> ([\d,]+)"


class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {
            "cmd_name": "slots",
            "cmd_arguments": None,
            "prefix": True,
            "checks": True,
            "retry_count": 0
        }
        self.turns_lost = 0


    async def cog_load(self):
        if not self.bot.config_dict["gamble"]["slots"]["enabled"]:
            try:
                await self.bot.unload_extension("cogs.slots")
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_slots(startup=True))

    async def start_slots(self, startup=False):
        try:
            if startup:
                await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["shortCooldown"]))
            else:
                self.bot.remove_queue(self.cmd)
                self.bot.log("queue removed - slots", "purple")
                await asyncio.sleep(self.bot.random_float(self.bot.config_dict["gamble"]["slots"]["cooldown"]))
            

            self.cmd["cmd_arguments"] = str(self.bot.config_dict["gamble"]["slots"]["startValue"]*(self.bot.config_dict["gamble"]["slots"]["multiplierOnLose"]**self.turns_lost))
            await self.bot.put_queue(self.cmd)
            self.bot.log("queue put slots", "purple")
        except Exception as e:
            print(e)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.id != 408785106942164992:
            return
        if before.channel.id != self.bot.channel_id:
            return
        
        if "slots" in after.content.lower():
            if "and won nothing... :c" in after.content:
                """Lose cash"""
                self.turns_lost+=1
                self.bot.log(f"lost slots", "green")
                await self.start_slots()
            else:
                if ("<:eggplant:417475705719226369>" in after.content.lower()
                and "and won" in after.content.lower()):
                    
                    """Didn't lose case but earned nothing"""
                    await self.start_slots()
                    self.bot.log(f"won nothing", "green")
                elif "and won" in after.content.lower():
                    """won cash"""
                    try:
                        match = int(re.search(won_pattern, after.content).group(1).replace(",",""))
                    except Exception as e:
                        print(e)
                        print("failed to fetch cf value, falling back!")
                        match = self.bot.config_dict["gamble"]["coinflip"]["startValue"]*2 #the 
                    self.bot.log(f"won slots by {match}", "green")
                    self.turns_lost = 0
                    await self.start_slots()


async def setup(bot):
    await bot.add_cog(Slots(bot))

