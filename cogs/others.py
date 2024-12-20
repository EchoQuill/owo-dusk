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
import random
import json
import re

from discord.ext import commands

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

class Others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - others","purple")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if "**you must accept these rules to use the bot!**" in message.content.lower():
                await asyncio.sleep(random.uniform(0.6,1.7))
                if message.components[0].children[0] and not message.components[0].children[0].disabled:
                    await message.components[0].children[0].click()
                self.bot.log(f"-{self.user}[+] Accepted OwO bot rules","spring_green1")
            elif "you currently have **__" in message.content:
                """task: add checks for cash at ready."""
                self.bot.balance = int(re.search(r'(\d{1,3}(?:,\d{3})*)(?= cowoncy)', re.sub(r'[*_]', '', message.content)).group(0).replace(',', ''))
                self.bot.log(f"{self.bot.user}[+] Checked for cash - {self.bot.balance} cowoncy!", "cyan3")
            """if "Create a team with the command `owo team add {animal}`" in message.content:
                self.bot.state = False
                await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["briefCooldown"]))
                await self.bot.send("zoo", bypass=True)"""
                
                


async def setup(bot):
    await bot.add_cog(Others(bot))