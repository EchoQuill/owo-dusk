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
import asyncio

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded


won_pattern = r"and won <:cowoncy:\d+> ([\d,]+)"
lose_pattern = r"bet <:cowoncy:\d+> ([\d,]+)"

"""
NOTE:
fix it spamming "won nothing"
"""

class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {
            "cmd_name": "slots",
            "cmd_arguments": None,
            "prefix": True,
            "checks": True,
            "retry_count": 0,
            "id": "slots"
        }
        self.turns_lost = 0
        self.exceeded_max_amount = False


    async def cog_load(self):
        if not self.bot.config_dict["gamble"]["slots"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.slots"))
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_slots(startup=True))

    async def cog_unload(self):
        await self.bot.remove_queue(id="slots")

    async def start_slots(self, startup=False):
        try:
            if startup:
                await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["briefCooldown"]))
            else:
                await self.bot.remove_queue(id="slots")
                await asyncio.sleep(self.bot.random_float(self.bot.config_dict["gamble"]["slots"]["cooldown"]))

            amount_to_gamble = self.bot.config_dict["gamble"]["slots"]["startValue"]*(self.bot.config_dict["gamble"]["slots"]["multiplierOnLose"]**self.turns_lost)
            if (amount_to_gamble <= self.bot.balance) and (not self.bot.gain_or_lose+self.bot.config_dict["gamble"]["allottedAmount"] <=0 ):
                if amount_to_gamble > 250000:
                    self.exceeded_max_amount = True
                else:
                    self.cmd["cmd_arguments"] = amount_to_gamble
                    await self.bot.put_queue(self.cmd)
            else:
                await self.start_slots()
        except Exception as e:
            print(e)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.id != 408785106942164992:
            return
        if before.channel.id != self.bot.channel_id:
            return
        if self.exceeded_max_amount:
            return
        
        if "slots" in after.content.lower():
            if "and won nothing... :c" in after.content:
                """Lose cash"""
                match = int(re.search(lose_pattern, after.content).group(1).replace(",",""))
                self.bot.balance-=match
                self.bot.gain_or_lose-=match
                self.turns_lost+=1
                await self.bot.log(f"lost {match} in slots, net profit - {self.bot.gain_or_lose}", "#ffafaf")
                await self.start_slots()
            else:
                if ("<:eggplant:417475705719226369>" in after.content.lower()
                and "and won" in after.content.lower()):
                    """Didn't lose case but earned nothing"""
                    await self.bot.log(f"didn't win or lose slots", "#ffafaf")
                    await self.start_slots()

                elif "and won" in after.content.lower():
                    """won cash"""
                    match = int(re.search(won_pattern, after.content).group(1).replace(",",""))
                    self.bot.balance+=match
                    self.bot.gain_or_lose+=match
                    self.turns_lost = 0
                    await self.bot.log(f"won {match} in slots, net profit - {self.bot.gain_or_lose}", "#ffafaf")
                    await self.start_slots()


async def setup(bot):
    await bot.add_cog(Slots(bot))

