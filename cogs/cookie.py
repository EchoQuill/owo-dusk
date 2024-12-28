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
def load_dict():
    global accounts_dict
    accounts_dict = load_json_dict()
load_dict()


class Cookie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {
            "cmd_name": "cookie",
            "cmd_arguments": f"<@{self.bot.config_dict['commands']['cookie']['userid']}>" if self.bot.config_dict["commands"]["cookie"]["pingUser"] else "",
            "prefix": True,
            "checks": True,
            "retry_count": 0
        }
    
    """change to conver times"""
    def time_in_seconds(self, time_to_convert=None):
        if time_to_convert is None:
            time_to_convert = datetime.now(timezone.utc).astimezone(pytz.timezone('US/Pacific'))
        return time_to_convert.timestamp()

    async def start_cookie(self):
        if str(self.bot.user.id) in accounts_dict:
            self.bot.log("cookie - 0", "honeydew2")
            self.current_time_seconds = self.time_in_seconds()
            self.last_cookie_time = accounts_dict[str(self.bot.user.id)].get("cookie", 0)

            # Time difference calculation
            self.time_diff = self.current_time_seconds - self.last_cookie_time

            if self.time_diff < 0:
                self.last_cookie_time = self.current_time_seconds
            if self.time_diff < 86400:  # 86400 = seconds till a day(24hrs).
                await asyncio.sleep(self.bot.calc_time())  # Wait until next 12:00 AM PST

            await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["shortCooldown"]))
            await self.bot.put_queue(self.cmd, priority=True)
            self.bot.log("put to queue - cookie", "honeydew2")

            with lock:
                load_dict()
                accounts_dict[str(self.bot.user.id)]["cookie"] = self.time_in_seconds()
                with open("utils/stats.json", "w") as f:
                    json.dump(accounts_dict, f, indent=4)

    async def cog_load(self):
        if not self.bot.config_dict["commands"]["cookie"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.cookie"))
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_cookie())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if "You got a cookie from" in message.content or "Nu! You need to wait" in message.content:
                self.bot.remove_queue(self.cmd)

                await asyncio.sleep(self.bot.calc_time())
                await asyncio.sleep(self.random_float(self.bot.config_dict["defaultCooldowns"]["moderateCooldown"]))
                await self.bot.put_queue(self.cmd, priority=True)
                self.bot.log("put to queue - cookie", "honeydew2")
                with lock:
                    load_dict()
                    accounts_dict[str(self.bot.user.id)]["cookie"] = self.time_in_seconds()
                    with open("utils/stats.json", "w") as f:
                        json.dump(accounts_dict, f, indent=4)


        
                
async def setup(bot):
    await bot.add_cog(Cookie(bot))