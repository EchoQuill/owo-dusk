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
import pytz
import asyncio
import threading

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded
from datetime import datetime, timezone

def load_json_dict(file_path="utils/stats.json"):
    with open(file_path, "r") as config_file:
        return json.load(config_file)

lock = threading.Lock()
accounts_dict = load_json_dict()
config_dict = load_json_dict("config.json")


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - daily","purple")
    
    """change to conver times"""
    def time_in_seconds(self, time_to_convert=None):
        if time_to_convert is None:
            time_to_convert = datetime.now(timezone.utc).astimezone(pytz.timezone('US/Pacific'))
        return time_to_convert.timestamp()
    
    async def start_daily(self):
        if str(self.bot.user.id) in accounts_dict:
            self.bot.log("daily - 0", "honeydew2")
            self.current_time_seconds = self.time_in_seconds()
            self.last_daily_time = accounts_dict[str(self.bot.user.id)].get("daily", 0)

            # Time difference calculation
            self.time_diff = self.current_time_seconds - self.last_daily_time
            print(self.current_time_seconds, self.last_daily_time)
            print(self.time_diff, "time diff")

            if self.time_diff < 0:
                self.last_daily_time = self.current_time_seconds
            if self.time_diff < 86400:  # 86400 = seconds till a day(24hrs).
                print(self.bot.calc_time())
                await asyncio.sleep(self.bot.calc_time())  # Wait until next 12:00 AM PST

            await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["briefCooldown"]))
            self.bot.queue.put("daily")
            self.bot.log("put to queue - Daily", "honeydew2")

            with lock:
                accounts_dict[str(self.bot.user.id)]["daily"] = self.time_in_seconds()
                with open("utils/stats.json", "w") as f:
                    json.dump(accounts_dict, f, indent=4)

    async def cog_load(self):
        self.bot.log(f"daily - start", "purple")
        if not config_dict["autoDaily"]:
            try:
                await self.bot.unload_extension("cogs.daily")
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_daily())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if "Here is your daily **<:cowoncy:416043450337853441>" in message.content:
                """Task: add cash check regex here"""
                self.bot.remove_queue("daily")
                print(self.bot.calc_time())
                await asyncio.sleep(self.bot.calc_time())
                await asyncio.sleep(self.random_float(config_dict["defaultCooldowns"]["moderateCooldown"]))
                self.bot.queue.put("daily")
                self.bot.log("put to queue - Daily", "honeydew2")
                with lock:
                    accounts_dict[str(self.bot.user.id)]["daily"] = self.time_in_seconds()
                    with open("utils/stats.json", "w") as f:
                        json.dump(accounts_dict, f, indent=4)

            if "**⏱ |** Nu! **" in message.content and "! You need to wait" in message.content:
                self.bot.log("Nu - Daily", "honeydew2")
                self.bot.remove_queue("daily")
                print(self.bot.calc_time())
                await asyncio.sleep(self.bot.calc_time())
                await asyncio.sleep(self.random_float(config_dict["defaultCooldowns"]["moderateCooldown"]))
                self.bot.queue.put("daily")
                self.bot.log("put to queue - Daily", "honeydew2")
                with lock:
                    accounts_dict[str(self.bot.user.id)]["daily"] = self.time_in_seconds()
                    with open("utils/stats.json", "w") as f:
                        json.dump(accounts_dict, f, indent=4)
                
async def setup(bot):
    await bot.add_cog(Daily(bot))