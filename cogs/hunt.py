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
import json
import re

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded


try:
    with open("utils/emojis.json", 'r', encoding="utf-8") as file:
        emoji_dict = json.load(file)
except FileNotFoundError:
    print("The file emojis.json was not found.")
except json.JSONDecodeError:
    print("Failed to decode JSON from the file.")


def get_emoji_cost(text, emoji_dict=emoji_dict):
    pattern = re.compile(r"<a:[a-zA-Z0-9_]+:[0-9]+>|:[a-zA-Z0-9_]+:|[\U0001F300-\U0001F6FF\U0001F700-\U0001F77F]")
    emojis = pattern.findall(text)
    emoji_names = [emoji_dict[char]["sell_price"] for char in emojis if char in emoji_dict]
    return emoji_names

def get_emoji_values(text):
    emoji_costs = get_emoji_cost(text)
    total_sell_price = 0

    for sell_price in emoji_costs:
        total_sell_price += sell_price

    return total_sell_price




class Hunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {
            "cmd_name": "",
            "prefix": True,
            "checks": True,
            "id": "hunt",
            "slash_cmd_name": "hunt",
            "removed": False
        }

    async def cog_load(self):
        if not self.bot.settings_dict["commands"]["hunt"]["enabled"] or self.bot.settings_dict["defaultCooldowns"]["reactionBot"]["hunt_and_battle"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.hunt"))
            except ExtensionNotLoaded:
                pass
        else:
            self.cmd["cmd_name"] = (
                self.bot.alias["hunt"]["shortform"] 
                if self.bot.settings_dict["commands"]["hunt"]["useShortForm"] 
                else self.bot.alias["hunt"]["alias"]
            )
            asyncio.create_task(self.bot.put_queue(self.cmd))

    async def cog_unload(self):
        await self.bot.remove_queue(id="hunt")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
                if 'you found:' in message.content.lower() or "caught" in message.content.lower():
                    await self.bot.remove_queue(id="hunt")

                    msg_lines = message.content.splitlines()

                    sell_value = get_emoji_values(msg_lines[0] if "caught" in message.content.lower() else msg_lines[1])
                    await self.bot.update_cash(sell_value - 5, assumed=True)
                    await self.bot.update_cash(5, reduce=True)

                    await self.bot.sleep_till(self.bot.settings_dict["commands"]["hunt"]["cooldown"])
                    self.cmd["cmd_name"] = (
                        self.bot.alias["hunt"]["shortform"] 
                        if self.bot.settings_dict["commands"]["hunt"]["useShortForm"] 
                        else self.bot.alias["hunt"]["alias"]
                    )
                    await self.bot.put_queue(self.cmd)
        except Exception as e:
            await self.bot.log(f"Error - {e}, During hunt on_message()", "#c25560")

async def setup(bot):
    await bot.add_cog(Hunt(bot))
