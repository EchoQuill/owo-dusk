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


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id in [self.bot.user.id, 1209017744696279041] + self.bot.config_dict["textCommands"]["allowedUsers"]:
            if f"{self.bot.config_dict["textCommands"]["prefix"]}{self.bot.config_dict["textCommands"]["commandToStopUser"]}" in message.content.lower():
                await self.bot.log("stopping owo-dusk..","#87875f")
                self.bot.state=False

            elif f"{self.bot.config_dict["textCommands"]["prefix"]}{self.bot.config_dict["textCommands"]["commandToStartUser"]}" in message.content.lower():
                await self.bot.log("starting owo-dusk..","#87875f")
                self.bot.state=True


async def setup(bot):
    await bot.add_cog(Chat(bot))