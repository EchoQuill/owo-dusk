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

from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print("loaded!")

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        """
        https://discordpy-self.readthedocs.io/en/latest/api.html?highlight=on_socket_raw_receive#discord.on_socket_raw_receive
        For this to work enable_debug_events argument was passed as True in client.
        """
        # Note: msg is of string datatype.

        # Only parse JSON if channel id.
        if f'"channel_id":"{self.bot.channel_id}"' in msg:
            parsed_msg = json.loads(msg)



async def setup(bot):
    await bot.add_cog(Test(bot))
