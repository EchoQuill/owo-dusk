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
        if not self.bot.captcha:
            await self.bot.upd_cmd_state(cmd["id"])
            await self.bot.send(f"{self.bot.config_dict['setprefix'] if prefix else ''}{cmd["name"]}")

    async def startup_handler(self):
        print("yp")
        await self.bot.set_stat(False)
        print("np")
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
        hunt_cmd = {"name":self.bot.alias["hunt"]["normal" if not hunt_shortform else "shortform"], "id": "hunt"}
        battle_cmd = {"name":self.bot.alias["battle"]["normal" if not battle_shortform else "shortform"], "id": "battle"}
        owo_cmd = {"name":self.bot.alias["owo"]["normal"], "id": "owo"}
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
            await self.send_cmd(hunt_cmd)
            await self.send_cmd(battle_cmd)
        else:
            cmd = hunt_cmd if hunt else battle_cmd
            await self.send_cmd(cmd)

        """OwO/UwU"""
        if reaction_bot_dict["owo"] and commands_dict["owo"]["enabled"]:
            print("owo")
            await self.send_cmd(owo_cmd, prefix=False)

        """Pray/Curse"""
        if pray or curse:
            print("pray/curse")
            cmds = []
            if pray:
                cmds.append("pray")
            if curse:
                cmds.append("curse")
            cmd = {"name": random.choice(cmds), "id": "pray"}

            await self.send_cmd(cmd)
        await self.bot.set_stat(True)

    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        """TASK: Double check"""
        asyncio.create_task(self.startup_handler())


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
                owo_cmd = {"name":self.bot.alias["owo"]["normal"], "id": "owo"}
                await self.bot.sleep_till(reaction_bot_dict["cooldown"])
                await self.send_cmd(owo_cmd, prefix=False)

            elif "**hunt/battle**" in message.content and (hunt or battle):
                hunt_shortform = commands_dict["hunt"]["useShortForm"] 
                battle_shortform = commands_dict["battle"]["useShortForm"] 
                hunt_cmd = {"name":self.bot.alias["hunt"]["normal" if not hunt_shortform else "shortform"], "id": "hunt"}
                battle_cmd = {"name":self.bot.alias["battle"]["normal" if not battle_shortform else "shortform"], "id": "battle"}

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
                cmd = {"name": random.choice(cmds), "id": "pray"}

                await self.send_cmd(cmd)


async def setup(bot):
    await bot.add_cog(Reactionbot(bot))
