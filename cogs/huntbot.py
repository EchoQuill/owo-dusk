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
from utils.hbCalc import allocate_essence

password_reset_regex = r"(?<=Password will reset in )(\d+)"
huntbot_time_regex = r"(\d+)([DHM])"

def fetch_level_and_progress(value):
    """Fetch level and essence investment from the given field.value"""
    pattern = r"Lvl (\d+) \[(\d+)\/\d+\]"
    match = re.search(pattern, value)
    """
    1: level
    2: essence investment
    """
    return int(match.group(1)), int(match.group(2))

def fetch_essence(name):
    """Fetch essence from the given field.name"""
    pattern = r"Animal Essence - `(\d{1,3}(?:,\d{3})*)`"
    match = re.search(pattern, name)
    return int(match.group(1).replace(",", ""))


class Huntbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.upgrade_event = asyncio.Event()
        self.cmd = {
            "cmd_name": self.bot.alias["huntbot"]["normal"],
            "cmd_arguments": "",
            "prefix": True,
            "checks": True,
            "retry_count": 0,
            "id": "huntbot",
        }

        self.upgrade_cmd = {
            "cmd_name": self.bot.alias["upgrade"]["normal"],
            "cmd_arguments": "",
            "prefix": True,
            "checks": True,
            "retry_count": 0,
            "id": "upgrade",
        }

        self.upgrade_details = {
            "essence": 0,
            "efficiency": {"enabled": False, "current_level": 0, "invested": 0},
            "duration": {"enabled": False, "current_level": 0, "invested": 0},
            "cost": {"enabled": False, "current_level": 0, "invested": 0},
            "gain": {"enabled": False, "current_level": 0, "invested": 0},
            "exp": {"enabled": False, "current_level": 0, "invested": 0},
            "radar": {"enabled": False, "current_level": 0, "invested": 0},
        }

        for trait, value in self.bot.config_dict["commands"]["autoHuntBot"]["upgrader"]["traits"].items():
            if value:
                self.upgrade_details[trait]["enabled"] = True


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
            if isinstance(timeToSleep, list):
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

        await self.bot.put_queue(self.cmd)

    async def upgrade_confirmation(self):
        await self.upgrade_event.wait()
        self.upgrade_event.clear()
        await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["briefCooldown"]))

    def get_experience(self, embed):
        for field in embed.fields:
            for trait in {"efficiency", "duration", "cost", "gain", "experience", "radar"}:
                if trait in field.name.lower():
                    level,essence = fetch_level_and_progress(field.value)
                    self.upgrade_details[trait]["current_level"] = level
                    self.upgrade_details[trait]["invested"] = essence
                    print(f"{trait}: level {level}, {essence}")
                    break
            if "essence" in field.name.lower():
                self.upgrade_details[trait]["current_level"] = fetch_essence(field.name)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != self.bot.cm.id:
            return
        if "Please include your password!" in message.content:
            total_seconds_hb = (
                int(re.findall(password_reset_regex, message.content)[0]) * 60
            )
            await self.bot.log(f"HB {total_seconds_hb} sp - pass", "#afaf87")
            await self.send_ah(timeToSleep=total_seconds_hb)

        elif "I WILL BE BACK IN" in message.content:
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

        elif "I AM BACK WITH" in message.content:
            if self.bot.config_dict["commands"]["autoHuntBot"]["upgrader"]["enabled"]:
                self.cmd["cmd_arguments"] = ""
                await self.bot.put_queue(self.cmd)
                await self.bot.log(f"huntbot back! attempting to upgrade huntbot..", "#afaf87")
            else:
                await self.send_ah(
                    timeToSleep=self.bot.config_dict["defaultCooldowns"]["briefCooldown"]
                )
                await self.bot.log(f"huntbot back! sending next huntbot command.", "#afaf87")

        elif "Here is your password!" in message.content:
            ans = await solveHbCaptcha(message.attachments[0].url, self.bot.session)
            await self.bot.log(f"HB 1 sp - {ans}", "#afaf87")
            await self.send_ah(
                timeToSleep=self.bot.config_dict["defaultCooldowns"]["briefCooldown"],
                ans=ans,
            )

        elif "You successfully upgraded" in message.content:
            self.upgrade_event.set()

        elif message.embeds:
            for embed in message.embeds:
                if embed.author and "'s huntbot" in embed.author.name.lower():
                    self.bot.state = False
                    print("lets go, upgrading")
                    await self.bot.remove_queue(id="huntbot")
                    if embed.fields:
                        print("field available")
                        self.get_experience(embed)
                        data = allocate_essence(self.upgrade_details)
                        await asyncio.sleep(self.bot.random_float(self.bot.config_dict["commands"]["autoHuntBot"]["upgrader"]["sleeptime"]))
                        for trait, essence_alloc in data.items():
                            self.upgrade_cmd["cmd_arguments"] = f"{trait} {essence_alloc}"
                            await self.bot.put_queue(self.upgrade_cmd)
                            await self.upgrade_confirmation()
                        self.bot.state = True
                    await self.send_ah(
                        timeToSleep=self.bot.config_dict["defaultCooldowns"]["briefCooldown"]
                    )


async def setup(bot):
    await bot.add_cog(Huntbot(bot))
