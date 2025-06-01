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


"""
REF :- 
gem code - https://github.com/ChristopherBThai/Discord-OwO-Bot/blob/master/src/commands/commandList/shop/inventory.js
small numbers - https://github.com/ChristopherBThai/Discord-OwO-Bot/blob/master/src/commands/commandList/shop/util/shopUtil.js
"""


gem_tiers = {
    "common": ["051", "065", "072", "079"],
    "uncommon": ["052", "066", "073", "080"],
    "rare": ["053", "067", "074", "081"],
    "epic": ["054", "068", "075", "082"],
    "mythical": ["055", "069", "076", "083"],
    "legendary": ["056", "070", "077", "084"],
    "fabled": ["057", "071", "078", "085"],
}


def convert_small_numbers(small_number):
    numbers = {
        "⁰": "0",
        "¹": "1",
        "²": "2",
        "³": "3",
        "⁴": "4",
        "⁵": "5",
        "⁶": "6",
        "⁷": "7",
        "⁸": "8",
        "⁹": "9",
    }
    normal_string = ''.join(numbers.get(char, char) for char in small_number)
    return int(normal_string)


def find_gems_available(message):

    available_gems = {
        "fabled": {"057": 0, "071": 0, "078": 0, "085": 0},  # fabled
        "legendary": {"056": 0, "070": 0, "077": 0, "084": 0},  # legendary
        "mythical": {"055": 0, "069": 0, "076": 0, "083": 0},  # mythical
        "epic": {"054": 0, "068": 0, "075": 0, "082": 0},  # epic
        "rare": {"053": 0, "067": 0, "074": 0, "081": 0},  # rare
        "uncommon": {"052": 0, "066": 0, "073": 0, "080": 0},  # uncommon
        "common": {"051": 0, "065": 0, "072": 0, "079": 0},  # common
        # hunt, emp, luck, special
    }
    """
    Example output:-
    [('050', '⁰⁷'), ('051', '⁰³')]
    """
    inv_numbers = re.findall(r"`(\d+)`.*?([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", message)
    for gem_id, small_number in inv_numbers:
        gem_count = convert_small_numbers(small_number)

        for _, gems in available_gems.items():
            if gem_id in gems:
                gems[gem_id] = gem_count
                break
    return available_gems


class Gems(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.grouped_gems = None
        self.available_gems = None
        self.inventory_check = False
        self.gem_cmd = {
            "cmd_name": self.bot.alias["use"]["normal"],
            "cmd_arguments": "",
            "prefix": True,
            "checks": False,
            "id": "gems"
        }
        self.inv_cmd = {
            "cmd_name": self.bot.alias["inv"]["normal"],
            "prefix": True,
            "checks": True,
            "id": "inv"
        }

    def find_gems_to_use(self, available_gems):
        gem_type = {
            0: "huntGem",
            1: "empoweredGem",
            2: "luckyGem",
            3: "specialGem"
        }
        tier_order = ['fabled', 'legendary', 'mythical', 'epic', 'rare', 'uncommon', 'common']
        cnf = self.bot.settings_dict["autoUse"]["gems"]

        if cnf["order"]["lowestToHighest"]:
            tier_order.reverse()

        grouped_gem_list = []

        for tier in tier_order:
            if not cnf["tiers"][tier]:
                continue

            current_group = []
            for gem_id in gem_tiers[tier]:
                gem_index = gem_tiers[tier].index(gem_id)
                gem_type_key = gem_type[gem_index]
                if cnf["gemsToUse"].get(gem_type_key) and available_gems[tier].get(gem_id, 0) > 0:
                    current_group.append(gem_id)

            if current_group:
                grouped_gem_list.append(current_group)

        return self.process_result(grouped_gem_list)


    def process_result(self, result):
        print(f"Resulting gem groups: {result}")
        
        # Find the group with the highest number of items
        max_group = max(result, key=len, default=None)
        
        if max_group:
            print(f"Selected group with the highest count: {max_group}")
        else:
            print("No groups found.")
        print(max_group)
        
        return max_group



    async def cog_load(self):
        if not self.bot.settings_dict["commands"]["hunt"]["enabled"] or not self.bot.settings_dict["autoUse"]["gems"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.gems"))
            except ExtensionNotLoaded:
                pass

    async def cog_unload(self):
        await self.bot.remove_queue(id="gems")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != self.bot.channel_id or message.author.id != self.bot.owo_bot_id:
            return
        
        if "caught" in message.content:
            if self.bot.user_status["no_gems"]:
                return
            await self.bot.set_stat(False)
            self.inventory_check = True
            await self.bot.put_queue(self.inv_cmd, priority=True)
        elif "'s Inventory ======**" in message.content:
            if self.inventory_check:
                await self.bot.remove_queue(id="inv")
                #if not self.available_gems:
                self.available_gems = find_gems_available(message.content)
                gems_list = self.find_gems_to_use(self.available_gems)

                self.gem_cmd["cmd_arguments"]=""
                if gems_list:
                    for i in gems_list:
                        self.gem_cmd["cmd_arguments"]+=f"{i[1:]} "
                else:
                    await self.log(f"Warn: No gems to use.", "#924444")
                    self.bot.user_status["no_gems"] = True
                await self.bot.put_queue(self.gem_cmd, priority=True)
                await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["briefCooldown"])
                await self.bot.set_stat(True)
                self.inventory_check = False

async def setup(bot):
    await bot.add_cog(Gems(bot))
