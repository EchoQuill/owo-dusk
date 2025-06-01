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
            "cmd_name": self.bot.alias["cookie"]["normal"],
            "cmd_arguments": "",
            "prefix": True,
            "checks": True,
            "id": "cookie"
        }
    
    """change to conver times"""
    

    async def start_cookie(self):
        if str(self.bot.user.id) in accounts_dict:
            self.current_time_seconds = self.bot.time_in_seconds()
            self.last_cookie_time = accounts_dict[str(self.bot.user.id)].get("cookie", 0)

            # Time difference calculation
            self.time_diff = self.current_time_seconds - self.last_cookie_time

            if self.time_diff < 0:
                self.last_cookie_time = self.current_time_seconds
            if self.time_diff < 86400:  # 86400 = seconds till a day(24hrs).
                await asyncio.sleep(self.bot.calc_time())  # Wait until next 12:00 AM PST

            await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["briefCooldown"])
            cnf = self.bot.settings_dict['commands']['cookie']
            self.cmd["cmd_arguments"] = f"<@{cnf['userid']}>" if cnf["pingUser"] else f"{cnf['userid']}"
            await self.bot.put_queue(self.cmd, priority=True)
            with lock:
                load_dict()
                accounts_dict[str(self.bot.user.id)]["cookie"] = self.bot.time_in_seconds()
                with open("utils/stats.json", "w") as f:
                    json.dump(accounts_dict, f, indent=4)

    async def cog_load(self):
        if not self.bot.settings_dict["commands"]["cookie"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.cookie"))
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_cookie())

    async def cog_unload(self):
        await self.bot.remove_queue(id="cookie")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if "You got a cookie from" in message.content or "Nu! You need to wait" in message.content:
                """
                'Nu! You need to wait' will get triggered unlike slow down one
                as the actual command slowdown is different from this.
                """
                await self.bot.remove_queue(id="cookie")

                await asyncio.sleep(self.bot.calc_time())
                await asyncio.sleep(self.random_float(self.bot.settings_dict["defaultCooldowns"]["moderateCooldown"]))
                await self.bot.put_queue(self.cmd, priority=True)
                with lock:
                    load_dict()
                    accounts_dict[str(self.bot.user.id)]["cookie"] = self.bot.time_in_seconds()
                    with open("utils/stats.json", "w") as f:
                        json.dump(accounts_dict, f, indent=4)


        
                
async def setup(bot):
    await bot.add_cog(Cookie(bot))