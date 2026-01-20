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

from discord.ext import commands
import threading
import asyncio
import json

import components_v2 as comp

def load_json_dict(file_path="utils/stats.json"):
    with open(file_path, "r") as config_file:
        return json.load(config_file)

lock = threading.Lock()
def load_dict():
    global accounts_dict
    accounts_dict = load_json_dict()
load_dict()

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clicked = False

    async def cog_load(self):
        print("loaded!")

    async def fetch_json(self):
        if str(self.bot.user.id) in accounts_dict:
            self.current_time_seconds = self.bot.time_in_seconds()
            self.last_daily_time = accounts_dict[str(self.bot.user.id)].get("daily", 0)

            # Time difference calculation
            self.time_diff = self.current_time_seconds - self.last_daily_time

            if self.time_diff < 0:
                self.last_daily_time = self.current_time_seconds
            if self.time_diff < 86400:  # 86400 = seconds till a day(24hrs).
                await asyncio.sleep(self.bot.calc_time())  # Wait until next 12:00 AM PST

            await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["briefCooldown"])

            with lock:
                load_dict()
                accounts_dict[str(self.bot.user.id)]["daily"] = self.bot.time_in_seconds()
                with open("utils/stats.json", "w") as f:
                    json.dump(accounts_dict, f, indent=4)

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        """
        https://discordpy-self.readthedocs.io/en/latest/api.html?highlight=on_socket_raw_receive#discord.on_socket_raw_receive
        For this to work enable_debug_events argument was passed as True in client.

        Right now we are getting the message object directly through on_socket_raw_receive 
        we may want to consider getting message once and sharing them instead to reduce unneccesory parsing of raw input.
        """
        if self.clicked:
            return
        
        parsed_msg = json.loads(msg)
        if parsed_msg["t"] != "MESSAGE_CREATE":
            return

        message = comp.message.get_message_obj(parsed_msg["d"])

        if (
            message.author.id == self.bot.owo_bot_id
        ):
            if message.components:
                for component in message.components:
                    # Boss Embed
                    if component.component_name == "section":
                        if component.component[0].content and "runs away" in component.component[0].content:
                            await self.bot.log("Boss component Detected!", "#B5C1CE")
                            # Boss Fight button
                            if component.accessory and component.accessory.component_name == "button":
                                if component.accessory.custom_id == "guildboss_fight":
                                    boss_channel = await self.bot.fetch_channel(message.channel_id)
                                    await self.bot.log("Boss component - clicking..", "#B5C1CE")
                                    await asyncio.sleep(0.5) 
                                    await component.accessory.click(
                                        self.bot.ws.session_id,
                                        self.bot.local_headers,
                                        boss_channel.guild.id
                                    )
                                    await self.bot.log("Boss component - clicked!", "#B5C1CE")
                                    self.clicked = True



async def setup(bot):
    await bot.add_cog(Boss(bot))
