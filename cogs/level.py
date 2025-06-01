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
import string
import random

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded



quotes_url = "https://favqs.com/api/qotd"

def generate_random_string(min, max):
    """something like a list?"""
    characters = string.ascii_lowercase + ' '
    length = random.randint(min,max)
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string

async def fetch_quotes(session):
    async with session.get(quotes_url) as response:
        if response.status == 200:
            data = await response.json()
            quote = data["quote"]["body"]  # data[0]["quote"]
            return quote



class Level(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot
        self.last_level_grind_message = None
        self.cmd = {
            "cmd_name": None,
            "prefix": False,
            "checks": True,
            "id": "level"
        }

    async def start_level_grind(self):
        #await asyncio.sleep(1)
        await self.bot.remove_queue(id="level")
        cnf = self.bot.settings_dict["commands"]["lvlGrind"]
        try:
            await self.bot.sleep_till(cnf["cooldown"])
            if cnf["useQuoteInstead"]:
                self.last_level_grind_message = await fetch_quotes(self.bot.session)
            else:
                self.last_level_grind_message = generate_random_string(cnf["minLengthForRandomString"], cnf["maxLengthForRandomString"])
            self.cmd["cmd_name"] = self.last_level_grind_message

            await self.bot.put_queue(self.cmd)
        except Exception as e:
            await self.bot.log(f"Error - start_level_grind(): {e}", "#c25560")
        
    
    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if not self.bot.settings_dict["commands"]["lvlGrind"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.level"))
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_level_grind())

    async def cog_unload(self):
        await self.bot.remove_queue(id="level")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.user.id:
            if self.last_level_grind_message == message.content:
                await self.start_level_grind()
                

async def setup(bot):
    await bot.add_cog(Level(bot))