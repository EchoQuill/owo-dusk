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

    def fetch_cmd(self, id):
        commands_dict = self.bot.settings_dict["commands"]
        hunt_shortform = commands_dict["hunt"]["useShortForm"] 
        battle_shortform = commands_dict["battle"]["useShortForm"] 

        cmd_name = {
            "hunt": self.bot.alias["hunt"]["normal" if not hunt_shortform else "shortform"],
            "battle": self.bot.alias["battle"]["normal" if not battle_shortform else "shortform"],
            "owo": self.bot.alias["owo"]["normal"]
        }

        base = {
            "cmd_name": cmd_name.get(id, id),
            "prefix": id != "owo",
            "checks": False,
            "id": id if id!="curse" else "pray"
        }

        return base

    async def send_cmd(self, cmd):
        await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["reactionBot"]["cooldown"])
        await self.bot.put_queue(self.fetch_cmd(cmd), quick=True, priority=True)

    async def startup_handler(self):
        await self.bot.set_stat(False)
        """
        Usually pattern goes like
        owoh
        owob
        owo
        pray/curse
        From what I have seen people do.
        """
        reaction_bot_dict = self.bot.settings_dict["defaultCooldowns"]["reactionBot"]
        commands_dict = self.bot.settings_dict["commands"]
        """Define alias of commands"""
        print("init")

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
            print("hb rr")
            await self.send_cmd("hunt")
            await self.send_cmd("battle")
        else:
            cmd = "hunt" if hunt else "battle"
            await self.send_cmd(cmd)

        """OwO/UwU"""
        if reaction_bot_dict["owo"] and commands_dict["owo"]["enabled"]:
            await self.send_cmd("owo")

        """Pray/Curse"""
        if pray or curse:
            print("pray/curse")
            cmds = []
            if pray:
                cmds.append("pray")
            if curse:
                cmds.append("curse")
            await self.send_cmd(random.choice(cmds))
        await self.bot.set_stat(True)

    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        """TASK: Double check"""
        reaction_bot_dict = self.bot.settings_dict["defaultCooldowns"]["reactionBot"]
        commands_dict = self.bot.settings_dict["commands"]
        hunt = commands_dict["hunt"]["enabled"]
        battle = commands_dict["battle"]["enabled"]
        pray = commands_dict["pray"]["enabled"]
        curse = commands_dict["curse"]["enabled"]
        owo = commands_dict["owo"]["enabled"]
        if (reaction_bot_dict["hunt_and_battle"] or reaction_bot_dict["pray_and_curse"] or reaction_bot_dict["owo"]) and (hunt or battle or pray or curse or owo):
            asyncio.create_task(self.startup_handler())
        else:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.reactionbot"))
            except ExtensionNotLoaded:
                pass


    @commands.Cog.listener()
    async def on_message(self, message):
        
        reaction_bot_dict = self.bot.settings_dict["defaultCooldowns"]["reactionBot"]
        commands_dict = self.bot.settings_dict["commands"]
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
                await self.send_cmd("owo")

            elif "**hunt/battle**" in message.content and (hunt or battle):
                if hunt and battle:
                    print("hb rr")
                    await self.send_cmd("hunt")
                    await self.send_cmd("battle")
                else:
                    cmd = "hunt" if hunt else "battle"
                    await self.send_cmd(cmd)

            elif "**pray/curse**" in message.content and (pray or curse):
                cmds = []
                if pray:
                    cmds.append("pray")
                if curse:
                    cmds.append("curse")
                await self.send_cmd(random.choice(cmds))


async def setup(bot):
    await bot.add_cog(Reactionbot(bot))
