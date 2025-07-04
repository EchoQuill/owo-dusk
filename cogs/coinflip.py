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


won_pattern = r"you won \*\*<:cowoncy:\d+> ([\d,]+)"
lose_pattern = r"spent \*\*<:cowoncy:\d+> ([\d,]+)"


class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {
            "cmd_name": self.bot.alias["coinflip"]["normal"],
            "cmd_arguments": None,
            "prefix": True,
            "checks": True,
            
            "id": "coinflip"
        }
        self.turns_lost = 0
        self.exceeded_max_amount = False

        self.gamble_flags = {
            "goal_reached": False,
            "amount_exceeded": False,
            "no_balance": False
        }


    async def cog_load(self):
        if not self.bot.settings_dict["gamble"]["coinflip"]["enabled"]:
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
        cnf = self.bot.settings_dict["gamble"]["coinflip"]
        goal_system_dict = self.bot.settings_dict['gamble']['goalSystem']
        try:
            if startup:
                await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["briefCooldown"])
            else:
                await self.bot.remove_queue(id="coinflip")
                await self.bot.sleep_till(cnf["cooldown"])
            
            amount_to_gamble = int(cnf["startValue"]*(cnf["multiplierOnLose"]**self.turns_lost))

            # Goal system check
            if goal_system_dict["enabled"] and self.bot.gain_or_lose > goal_system_dict["amount"]:
                if not self.gamble_flags["goal_reached"]:
                    self.gamble_flags["goal_reached"] = True
                    await self.bot.log(f"goal reached - {self.bot.gain_or_lose}/{cnf['amount']}, stopping coinflip!", "#4a270c")

                return await self.start_cf()
            elif self.gamble_flags["goal_reached"]:
                self.gamble_flags["goal_reached"] = False

            # Balance check
            if amount_to_gamble > self.bot.user_status["balance"] and not self.bot.settings_dict["cashCheck"]:
                if not self.gamble_flags["no_balance"]:
                    self.gamble_flags["no_balance"] = True
                    await self.bot.log(f"Amount to gamle next ({amount_to_gamble}) exceeds bot balance ({self.bot.user_status["balance"]}), stopping coinflip!", "#4a270c")

                return await self.start_cf()
            elif self.gamble_flags["no_balance"]:
                await self.bot.log(f"Balance regained! ({self.bot.user_status["balance"]}) - restarting coinflip!", "#4a270c")
                self.gamble_flags["no_balance"] = False

            # Allotted value check
            if (self.bot.gain_or_lose + (self.bot.settings_dict["gamble"]["allottedAmount"] - amount_to_gamble) <=0):
                if not self.gamble_flags["amount_exceeded"]:
                    self.gamble_flags["amount_exceeded"] = True
                    await self.bot.log(f"Allotted value ({self.bot.settings_dict["gamble"]["allottedAmount"]}) exceeded, stopping coinflip!", "#4a270c")

                return await self.start_cf()
            elif self.gamble_flags["amount_exceeded"]:
                self.gamble_flags["amount_exceeded"] = False

            
            if amount_to_gamble > 250000:
                self.exceeded_max_amount = True
            else:
                self.cmd["cmd_arguments"] = str(amount_to_gamble)
                if cnf["options"]:
                    self.cmd["cmd_arguments"]+=f" {self.bot.random.choice(cnf['options'])}"
                await self.bot.put_queue(self.cmd)

        except Exception as e:
            await self.bot.log(f"Error - {e}, During coinflip start_cf()", "#c25560")


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.id != 408785106942164992:
            return
        if before.channel.id != self.bot.channel_id:
            return
        if self.exceeded_max_amount:
            return
        
        if "chose" in after.content.lower():
            try:
                if "and you lost it all... :c" in after.content.lower():
                    self.turns_lost+=1
                    match = int(re.search(lose_pattern, after.content).group(1).replace(",",""))

                    await self.bot.update_cash(match, reduce=True)
                    self.bot.gain_or_lose-=match

                    await self.bot.log(f"lost {match} in cf, net profit - {self.bot.gain_or_lose}", "#ffafaf")
                    await self.start_cf()
                    await self.bot.update_gamble_db("losses")
                else:
                    won_match = int(re.search(won_pattern, after.content).group(1).replace(",",""))
                    lose_match = int(re.search(lose_pattern, after.content).group(1).replace(",",""))
                    self.turns_lost = 0
                    profit = won_match-lose_match

                    await self.bot.update_cash(profit)
                    self.bot.gain_or_lose+=profit
                    
                    await self.bot.log(f"won {won_match} in cf, net profit - {self.bot.gain_or_lose}", "#ffafaf")
                    await self.start_cf()
                    await self.bot.update_gamble_db("wins")
            except Exception as e:
                await self.bot.log(f"Error - {e}, During coinflip on_message_edit()", "#c25560")

async def setup(bot):
    await bot.add_cog(Coinflip(bot))

