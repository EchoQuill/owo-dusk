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



try:
    with open("utils/emojis.json", 'r', encoding="utf-8") as file:
        emoji_dict = json.load(file)
except FileNotFoundError:
    print("The file emojis.json was not found.")
except json.JSONDecodeError:
    print("Failed to decode JSON from the file.")


def get_emoji_names(text, emoji_dict=emoji_dict):
    pattern = re.compile(r"<a:[a-zA-Z0-9_]+:[0-9]+>|:[a-zA-Z0-9_]+:|[\U0001F300-\U0001F6FF\U0001F700-\U0001F77F]")
    emojis = pattern.findall(text)
    emoji_names = [emoji_dict[char]["name"] for char in emojis if char in emoji_dict]
    return emoji_names


class Others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.zoo = False
        self.lootbox_cmd = {
            "cmd_name": self.bot.alias["lootbox"]["normal"],
            "prefix": True,
            "checks": False,
            "slash_cmd_name": "lootbox",
            "id": "lootbox"
        }

        self.crate_cmd = {
            "cmd_name": self.bot.alias["crate"]["normal"],
            "prefix": True,
            "checks": False,
            "slash_cmd_name": "crate",
            "id": "crate"
        }
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:

            # Accept Rules
            if "**you must accept these rules to use the bot!**" in message.content.lower():
                await asyncio.sleep(self.bot.random.uniform(0.6,1.7))
                if message.components[0].children[0] and not message.components[0].children[0].disabled:
                    await message.components[0].children[0].click()

            # Cash Check
            elif "you currently have **__" in message.content:
                """task: add checks for cash at ready."""
                await self.bot.update_cash(
                    int(re.search(r'(\d{1,3}(?:,\d{3})*)(?= cowoncy)', re.sub(r'[*_]', '', message.content)).group(0).replace(',', '')),
                    override = True
                )
                await self.bot.log(f"Has {self.bot.user_status['balance']} cowoncy!", "#d787d7")
                await self.bot.remove_queue(id="cash")

            # Lootbox and Crate
            elif "** You received a **weapon crate**!" in message.content or "You found a **weapon crate**!" in message.content:
                if self.bot.settings_dict["autoUse"]["autoCrate"]:
                    await self.bot.put_queue(self.crate_cmd)
                
            elif "** You received a **lootbox**!" in message.content or "You found a **lootbox**!" in message.content:
                if self.bot.settings_dict["autoUse"]["autoLootbox"]:
                    await self.bot.put_queue(self.lootbox_cmd)
                    # give time for command to run
                    await asyncio.sleep(2.5)
                    self.bot.user_status["no_gems"] = False

            # Add animals to team
            elif "Create a team with the command `owo team add {animal}`" in message.content:
                await self.bot.set_stat(False)
                self.zoo = True
                team_cmd = {
                    "cmd_name": self.bot.alias["zoo"]["normal"],
                    "prefix": True,
                    "checks": False,
                    "retry_count": 0,
                    "id": "zoo"
                }
                await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["briefCooldown"])
                await self.bot.put_queue(team_cmd, priority=True)

            elif "s zoo! **" in message.content and self.zoo:
                animals = get_emoji_names(message.content)
                animals.reverse()
                await asyncio.sleep(self.bot.random.uniform(1.5,2.3))
                three_animals = min(len(animals), 3) #int
                for i in range(three_animals):
                    zoo_cmd = {
                        "cmd_name": "team",
                        "cmd_arguments": f"add {animals[i]}",
                        "prefix": True,
                        "checks": False,
                        "retry_count": 0
                    }
                    await self.bot.put_queue(zoo_cmd, priority=True)
                    await asyncio.sleep(self.bot.random.uniform(1.5,2.3))

                self.zoo = False
                await self.bot.set_stat(True)

async def setup(bot):
    await bot.add_cog(Others(bot))