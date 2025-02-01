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
import re

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded
from utils.huntBotSolver import solveHbCaptcha

password_reset_regex = r"(?<=Password will reset in )(\d+)"
huntbot_time_regex = r"(\d+)([DHM])"


class Huntbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {
            "cmd_name": "ah",
            "cmd_arguments": "",
            "prefix": True,
            "checks": True,
            "retry_count": 0,
            "id": "huntbot",
        }

    async def cog_load(self):
        if not self.bot.config_dict["commands"]["autoHuntBot"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.huntbot"))
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.send_ah(startup=True))

    async def cog_unload(self):
        await self.bot.remove_queue(id="huntbot")

    async def send_ah(self, startup=False, timeToSleep=None, ans=None):
        if startup:
            await asyncio.sleep(
                self.bot.random_float(
                    self.bot.config_dict["defaultCooldowns"]["briefCooldown"]
                )
            )
        else:
            await self.bot.remove_queue(id="huntbot")
            if type(timeToSleep, "list"):
                await asyncio.sleep(self.bot.random_float(timeToSleep))
            else:
                await asyncio.sleep(
                    self.bot.random_float([timeToSleep + 10, timeToSleep + 20])
                )

        """send the cmd"""
        self.cmd["cmd_arguments"] = str(
            self.bot.config_dict["commands"]["autoHuntBot"]["cashToSpend"]
        )
        if ans:
            self.cmd["cmd_arguments"] += f" {ans}"
            print(self.cmd["cmd_arguments"])

        await self.bot.put_queue(self.cmd)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Fail"""

        """**🚫 | user**, Please include your password! The command is `owo autohunt 4 {password}`!
**<:blank:427371936482328596> |** Password will reset in 9 minutes"""
        """**🚫 | user**, Wrong password! The command is `owo autohunt 4 {password}`!
**<:blank:427371936482328596> |** Password will reset in 10 minutes"""

        """Pass and wait"""

        """**<:cbot:459996048379609098> |** `BEEP BOOP. `**`user`**`, YOU SPENT 0 cowoncy`
**<:blank:427371936482328596> |** `I WILL BE BACK IN 0M WITH 0 ANIMALS,`
**<:blank:427371936482328596> |** `0 ESSENCE, AND 0 EXPERIENCE`"""

        """in progress"""

        """**<:cbot:459996048379609098> |** `BEEP BOOP. I AM STILL HUNTING. I WILL BE BACK IN 3M`
**<:blank:427371936482328596> |** `0% DONE | 0 ANIMALS CAPTURED`
**<:blank:427371936482328596> |** `[□□□□□□□□□□□□□□□□□□□□□□□□□]`"""

        """pass redo"""

        """**<:cbot:459996048379609098> |** `BEEP BOOP. I AM BACK WITH 1 ANIMALS,`
**<:blank:427371936482328596> |** `7 ESSENCE, AND 0 EXPERIENCE` 
<:uncommon:416520056269176842> **|** :rooster:¹"""

        if message.channel.id != self.bot.cm.id:
            return
        if "Please include your password!" in message.content:
            total_seconds_hb = (
                int(re.findall(password_reset_regex, message.content)[0]) * 60
            )
            await self.bot.log(f"HB {total_seconds_hb} sp - pass", "#afaf87")
            await self.send_ah(timeToSleep=total_seconds_hb)

        if "I WILL BE BACK IN" in message.content:
            total_seconds_hb = 0
            for amount, unit in re.findall(huntbot_time_regex, message.content):
                if unit == "M":
                    total_seconds_hb += int(amount) * 60
                elif unit == "H":
                    total_seconds_hb += int(amount) * 3600
                elif unit == "D":
                    total_seconds_hb += int(amount) * 86400
            await self.bot.log(f"HB {total_seconds_hb} sp - BACKIN", "#afaf87")
            await self.send_ah(timeToSleep=total_seconds_hb)

        if "I AM BACK WITH" in message.content:
            await self.send_ah(
                timeToSleep=self.bot.config_dict["defaultCooldowns"]["briefCooldown"]
            )
            await self.bot.log(f"HB 1 sp - BACKWITH", "#afaf87")

        if "Here is your password!" in message.content:
            ans = await solveHbCaptcha(message.attachments[0].url, self.bot.session)
            print(ans)
            await self.bot.log(f"HB 1 sp - {ans}", "#afaf87")
            await self.send_ah(
                timeToSleep=self.bot.config_dict["defaultCooldowns"]["briefCooldown"],
                ans=ans,
            )


async def setup(bot):
    await bot.add_cog(Huntbot(bot))
