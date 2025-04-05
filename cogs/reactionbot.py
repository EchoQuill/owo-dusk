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

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded


class Reactionbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_cmd(self, cmd, cooldown=None, prefix=True):
        await self.bot.sleep_till(cooldown or self.bot.config_dict["defaultCooldowns"]["reactionBot"]["cooldown"])
        if not self.bot.captcha and self.bot.state:
            await self.bot.upd_cmd_time()
            await self.bot.send(f"{self.bot.config_dict['setprefix'] if prefix else ''}{cmd}")

    async def startup_handler(self):
        """
        Usually pattern goes like
        owoh
        owob
        owo
        pray/curse
        From what I have seen people do.
        """
        reaction_bot_dict = self.bot.config_dict["defaultCooldowns"]["reactionBot"]
        commands_dict = self.bot.config_dict["commands"]
        hunt_shortform = commands_dict["hunt"]["useShortForm"] 
        battle_shortform = commands_dict["battle"]["useShortForm"] 

        """Define alias of commands"""
        hunt_cmd = self.bot.alias["hunt"]["normal" if not hunt_shortform else "shortform"]
        battle_cmd = self.bot.alias["battle"]["normal" if not battle_shortform else "shortform"]
        owo_cmd = self.bot.alias["owo"]["normal"]

        if reaction_bot_dict["hunt_and_battle"]:
            hunt = commands_dict["hunt"]["enabled"]
            battle = commands_dict["battle"]["enabled"]
        else:
            hunt, battle = False, False
        if reaction_bot_dict["pray_and_curse"]:
            pray = commands_dict["pray"]["enabled"]
            curse = commands_dict["curse"]["enabled"]
        else:
            pray, curse = False, False

        """Hunt/Battle"""
        if hunt and battle:
            await self.send_cmd(hunt_cmd)
            await self.send_cmd(battle_cmd)
        else:
            cmd = hunt_cmd if hunt else battle_cmd
            await self.send_cmd(cmd)

        """OwO/UwU"""
        await self.bot.sleep_till(reaction_bot_dict["cooldown"])
        await self.send_cmd(owo_cmd)

        """Pray/Curse"""
        cmds = []
        if pray:
            cmds.append("pray")
        if curse:
            cmds.append("curse")

        await self.send_cmd(self.bot.alias[random.choice(cmds)]["normal"])

    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if not self.bot.config_dict["commands"]["owo"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.reactionbot"))
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.startup_handler())

    async def cog_unload(self):
        self.send_owo.stop()

    @commands.Cog.listener()
    async def on_message(self, message):
        reaction_bot_dict = self.bot.config_dict["defaultCooldowns"]["reactionBot"]
        commands_dict = self.bot.config_dict["commands"]
        owo = reaction_bot_dict["owo"] and commands_dict["owo"]["enabled"]
        if reaction_bot_dict["hunt_and_battle"]:
            hunt = commands_dict["hunt"]["enabled"]
            battle = commands_dict["battle"]["enabled"]
        else:
            hunt, battle = False, False
        if reaction_bot_dict["pray_and_curse"]:
            pray = commands_dict["pray"]["enabled"]
            curse = commands_dict["curse"]["enabled"]
        else:
            pray, curse = False, False

        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.reaction_bot_id:
            """
            TASK: Add slash command support!
            """
            if "**OwO**" in message.content and owo:
                await self.bot.sleep_till(reaction_bot_dict["cooldown"])
                await self.send_cmd(self.bot.alias["owo"]["normal"])

            elif "**hunt/battle**" in message.content and (hunt or battle):
                hunt_shortform = commands_dict["hunt"]["useShortForm"] 
                battle_shortform = commands_dict["battle"]["useShortForm"] 
                hunt_cmd = self.bot.alias["hunt"]["normal" if not hunt_shortform else "shortform"]
                battle_cmd = self.bot.alias["battle"]["normal" if not battle_shortform else "shortform"]

                if hunt and battle:
                    await self.send_cmd(hunt_cmd)
                    await self.send_cmd(battle_cmd)
                else:
                    cmd = hunt_cmd if hunt else battle_cmd
                    await self.send_cmd(cmd)

            elif "**pray/curse**" in message.content and (pray or curse):
                cmds = []
                if pray:
                    cmds.append("pray")
                if curse:
                    cmds.append("curse")

                await self.send_cmd(self.bot.alias[random.choice(cmds)]["normal"])


async def setup(bot):
    await bot.add_cog(Reactionbot(bot))
