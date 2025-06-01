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
    if "[MAX]" in value:
        # Level 1000, will return max.
        return 1000, 0
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
        self.upgrade_event = asyncio.Event()
        self.cmd = {
            "cmd_name": self.bot.alias["huntbot"]["normal"],
            "cmd_arguments": "",
            "prefix": True,
            "checks": True,
            "id": "huntbot",
        }

        self.upgrade_cmd = {
            "cmd_name": self.bot.alias["upgrade"]["normal"],
            "cmd_arguments": "",
            "prefix": True,
            "checks": True,
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

        for trait, value in self.bot.settings_dict["commands"]["autoHuntBot"]["upgrader"]["traits"].items():
            if value:
                self.upgrade_details[trait]["enabled"] = True


    async def cog_load(self):
        if not self.bot.settings_dict["commands"]["autoHuntBot"]["enabled"]:
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
                    self.bot.settings_dict["defaultCooldowns"]["briefCooldown"]
                )+5
            )
        else:
            await self.bot.remove_queue(id="huntbot")
            if isinstance(timeToSleep, list):
                await self.bot.sleep_till(timeToSleep)
            else:
                """Task: add min noise if required"""
                await self.bot.sleep_till(timeToSleep, cd_list=False, noise=30)

        """send the cmd"""
        self.cmd["cmd_arguments"] = str(
            self.bot.settings_dict["commands"]["autoHuntBot"]["cashToSpend"]
        )
        if ans:
            self.cmd["cmd_arguments"] += f" {ans}"

        await self.bot.put_queue(self.cmd)

    async def upgrade_confirmation(self):
        await self.upgrade_event.wait()
        self.upgrade_event.clear()
        await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["briefCooldown"])

    def get_experience(self, embed):
        for field in embed.fields:
            for trait in {"efficiency", "duration", "cost", "gain", "exp", "radar"}:
                if trait in field.name.lower():
                    level,essence = fetch_level_and_progress(field.value)
                    self.upgrade_details[trait]["current_level"] = level
                    self.upgrade_details[trait]["invested"] = essence
                    break
            if "animal essence" in field.name.lower():
                self.upgrade_details["essence"] = fetch_essence(field.name)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != self.bot.cm.id:
            return
        if message.author.id != self.bot.owo_bot_id:
            return
        if "Please include your password!" in message.content:
            total_seconds_hb = (
                int(re.findall(password_reset_regex, message.content)[0]) * 60
            )
            await self.bot.log(f"huntbot stuck in password, retrying in {total_seconds_hb}s", "#afaf87")
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
            await self.bot.log(f"huntbot will be back in {total_seconds_hb}s", "#afaf87")
            await self.send_ah(timeToSleep=total_seconds_hb)

        elif "I AM BACK WITH" in message.content:
            if self.bot.settings_dict["commands"]["autoHuntBot"]["upgrader"]["enabled"]:
                await self.bot.remove_queue(id="huntbot")
                self.cmd["cmd_arguments"] = ""
                await self.bot.put_queue(self.cmd)
                await self.bot.log(f"huntbot back! attempting to upgrade huntbot..", "#afaf87")
            else:
                await self.send_ah(
                    timeToSleep=self.bot.settings_dict["defaultCooldowns"]["briefCooldown"]
                )
                await self.bot.log(f"huntbot back! sending next huntbot command.", "#afaf87")

        elif "Here is your password!" in message.content:
            ans = await solveHbCaptcha(message.attachments[0].url, self.bot.session)
            await self.bot.log(f"huntbot receieved password, attempting to solve!", "#afaf87")
            await self.send_ah(
                timeToSleep=self.bot.settings_dict["defaultCooldowns"]["briefCooldown"],
                ans=ans,
            )

        elif "You successfully upgraded" in message.content:
            self.upgrade_event.set()
            await self.bot.remove_queue(id="upgrade")

        elif message.embeds:
            for embed in message.embeds:
                if embed.author and "'s huntbot" in embed.author.name.lower():
                    await self.bot.remove_queue(id="huntbot")
                    await self.bot.set_stat(False)
                    if embed.fields:
                        self.get_experience(embed)
                        data = allocate_essence(self.upgrade_details, self.bot.settings_dict["commands"]["autoHuntBot"]["upgrader"]["priorities"])
                        await self.bot.sleep_till(self.bot.settings_dict["commands"]["autoHuntBot"]["upgrader"]["sleeptime"])
                        for trait, essence_alloc in data.items():
                            self.upgrade_cmd["cmd_arguments"] = f"{trait} {essence_alloc}"
                            if essence_alloc > 0:
                                print(self.upgrade_cmd["cmd_arguments"])
                                await self.bot.put_queue(self.upgrade_cmd, priority=True)
                                await self.upgrade_confirmation()
                                print(self.upgrade_details)
                        await self.bot.set_stat(True)
                    await self.send_ah(
                        timeToSleep=self.bot.settings_dict["defaultCooldowns"]["briefCooldown"]
                    )


async def setup(bot):
    await bot.add_cog(Huntbot(bot))
