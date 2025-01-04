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
    numbers = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9'}
    normal_string = ''.join(numbers.get(char, char) for char in small_number)
    return int(normal_string)



def find_gems_available(message):
    available_gems = {
        "057": 0, "071": 0, "078": 0, "085": 0, # fabled
        "056": 0, "070": 0, "077": 0, "084": 0, # legendary
        "055": 0, "069": 0, "076": 0, "083": 0, # mythical
        "054": 0, "068": 0, "075": 0, "082": 0, # epic
        "053": 0, "067": 0, "074": 0, "081": 0, # rare
        "052": 0, "066": 0, "073": 0, "080": 0, # uncommon
        "051": 0, "065": 0, "072": 0, "079": 0, # common
        # hunt, emp, luck, special
    }
    """
    Example output:-
    [('050', '⁰⁷'), ('051', '⁰³')]
    """
    inv_numbers = re.findall(r"`(\d+)`.*?([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", message)
    for item in inv_numbers:
        available_gems[item[0]] = convert_small_numbers(item[1])
    return available_gems

def get_gems_group(available_gems, config_dict):
    gem_type = {
        0: "huntGem",
        1: "empoweredGem",
        2: "luckyGem",
        3: "specialGem"
    }
    # Determine tier order
    tiers_ordered = list(gem_tiers.keys())
    print(tiers_ordered)
    if config_dict["autoUse"]["gems"]["order"]["lowestToHighest"]:
        tiers_ordered.reverse()
    
    gems_int = 0
    for i in config_dict["autoUse"]["gems"]["gemsToUse"].values():
        if i:
            print(i)
            gems_int+=1


    filtered_gems = []
    for tier in tiers_ordered:
        if config_dict["autoUse"]["gems"]["tiers"][tier]:
            for index, gem in enumerate(gem_tiers[tier]):
                if config_dict["autoUse"]["gems"]["gemsToUse"][gem_type[index]] and available_gems[gem] > 0:
                    
                    print(config_dict["autoUse"]["gems"]["gemsToUse"][gem_type[index]])
                    filtered_gems.append((tier, gem, available_gems[gem]))
    
    # Group gems by tier with a max size of 4
    grouped_gems = []
    current_group = []
    current_tier = None
    
    """Here _ is the count."""
    for tier, gem, _ in filtered_gems:
        if current_tier is None or current_tier == tier:
            print(current_group, " curr_group")
            print(gem, " gem")
            current_group.append(gem)
            current_tier = tier
            print(f"set current tier to {tier}")
        else:
            if len(current_group) < gems_int:
                print("current_group less than 4")
                current_group.append(gem)
                print(f"appended {gem} to current_group")
                print(current_group)
            if len(current_group) == gems_int:
                grouped_gems.append(current_group)
                print(f"appended current_group to grouped_gems")
                print(grouped_gems)
                current_group = [gem]
                current_tier = tier
    
    """Add the last group if it's not empty"""
    if current_group:
        grouped_gems.append(current_group)
    
    return grouped_gems


class Gems(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.grouped_gems = None
        self.available_gems = None
        self.gem_cmd = {
            "cmd_name": "use",
            "cmd_arguments": "",
            "prefix": True,
            "checks": False,
            "retry_count": 0,
            "id": "gems"
        }
        self.inv_cmd = {
            "cmd_name": "inv",
            "prefix": True,
            "checks": True,
            "retry_count": 0,
            "id": "gems"
        }

    async def cog_load(self):
        if not self.bot.config_dict["commands"]["hunt"]["enabled"] or not self.bot.config_dict["autoUse"]["gems"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.gems"))
            except ExtensionNotLoaded:
                pass

    async def cog_unload(self):
        self.bot.remove_queue(id="gems")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != self.bot.channel_id or message.author.id != self.bot.owo_bot_id:
            return
        #if "You found:" in message.content:
            #pass
        elif "caught" in message.content:
            await self.bot.put_queue(self.inv_cmd, priority=True)
        elif "'s Inventory ======**" in message.content:
            self.bot.remove_queue(self.inv_cmd)
            if not self.available_gems:
                self.available_gems = find_gems_available(message.content)
            self.grouped_gems = get_gems_group(self.available_gems, config_dict=self.bot.config_dict)
            for i in self.grouped_gems[0]:
                self.gem_cmd["cmd_arguments"]+=f" {i}"
            await self.bot.put_queue(self.gem_cmd, priority=True)
            await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["briefCooldown"]))
            self.bot.state = True

async def setup(bot):
    await bot.add_cog(Gems(bot))
