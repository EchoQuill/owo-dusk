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
import time

from discord.ext import commands, tasks
from discord.ext.commands import ExtensionNotLoaded


class Reactionbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd_states = {
            "hunt": 0,
            "battle": 0,
            "owo": 0,
            "pray": 0
        }

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
            "slash_cmd_name": id if id in {"hunt", "battle"} else None,
            "id": id if id!="curse" else "pray"
        }

        return base
    
    def check_cmd_state(self, cmd, return_dict=False):
        reaction_bot_dict = self.bot.settings_dict["defaultCooldowns"]["reactionBot"]
        commands_dict = self.bot.settings_dict["commands"]
        enabled_dict = {
            "hunt": commands_dict["hunt"]["enabled"] and reaction_bot_dict["hunt_and_battle"],
            "battle": commands_dict["battle"]["enabled"] and reaction_bot_dict["hunt_and_battle"],
            "owo": reaction_bot_dict["owo"] and commands_dict["owo"]["enabled"],
            "pray": commands_dict["pray"]["enabled"] and reaction_bot_dict["pray_and_curse"],
            "curse": commands_dict["curse"]["enabled"] and reaction_bot_dict["pray_and_curse"],
        }

        return enabled_dict.get(cmd) if not return_dict else enabled_dict
    
    def cmd_retry_required(self, cmd):
        cmd_id = cmd if cmd!="curse" else "pray"
        priority_dict = self.bot.misc["command_info"]
        last_time = self.cmd_states[cmd_id]
        # The 5s here is incase of delays.
        return (time.time() - last_time) > priority_dict[cmd_id]["basecd"]+5

    @tasks.loop(seconds=5)
    async def check_stuck_state(self):
        enabled_dict = self.check_cmd_state(cmd=None, return_dict=True)
        for cmd, state in enabled_dict.items():
            if state and self.cmd_retry_required(cmd):
                await self.send_cmd(cmd)

    async def send_cmd(self, cmd):
        await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["reactionBot"]["cooldown"])
        await self.bot.put_queue(self.fetch_cmd(cmd), quick=True, priority=True)
        self.cmd_states[cmd if cmd!="curse" else "pray"] = time.time()

    async def startup_handler(self):
        await self.bot.set_stat(False)
        """Define alias of commands"""
        hunt = self.check_cmd_state("hunt")
        battle = self.check_cmd_state("battle")
        pray = self.check_cmd_state("pray")
        curse = self.check_cmd_state("curse")

        """Hunt/Battle"""
        if hunt and battle:
            await self.send_cmd("hunt")
            await self.send_cmd("battle")
        else:
            cmd = "hunt" if hunt else "battle"
            await self.send_cmd(cmd)

        """OwO/UwU"""
        if self.check_cmd_state("owo"):
            await self.send_cmd("owo")

        """Pray/Curse"""
        if pray or curse:
            cmds = []
            if pray:
                cmds.append("pray")
            if curse:
                cmds.append("curse")
            await self.send_cmd(self.bot.random.choice(cmds))
        await self.bot.set_stat(True)
        """Start stuck state checker"""
        self.check_stuck_state.start()

    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        hunt = self.check_cmd_state("hunt")
        battle = self.check_cmd_state("battle")
        pray = self.check_cmd_state("pray")
        curse = self.check_cmd_state("curse")
        owo = self.check_cmd_state("owo")

        if hunt or battle or pray or curse or owo:
            asyncio.create_task(self.startup_handler())
        else:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.reactionbot"))
            except ExtensionNotLoaded:
                pass


    @commands.Cog.listener()
    async def on_message(self, message):
        hunt = self.check_cmd_state("hunt")
        battle = self.check_cmd_state("battle")
        pray = self.check_cmd_state("pray")
        curse = self.check_cmd_state("curse")
        owo = self.check_cmd_state("owo")

        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.reaction_bot_id:
            if "**OwO**" in message.content and (f"<@{self.bot.user.id}>" in message.content or self.bot.user.name in message.content) and owo:
                await self.send_cmd("owo")

            elif "**hunt/battle**" in message.content and (f"<@{self.bot.user.id}>" in message.content or self.bot.user.name in message.content) and (hunt or battle):
                if hunt and battle:
                    await self.send_cmd("hunt")
                    await self.send_cmd("battle")
                else:
                    cmd = "hunt" if hunt else "battle"
                    await self.send_cmd(cmd)

            elif "**pray/curse**" in message.content and (f"<@{self.bot.user.id}>" in message.content or self.bot.user.name in message.content) and (pray or curse):
                cmds = []
                if pray:
                    cmds.append("pray")
                if curse:
                    cmds.append("curse")
                await self.send_cmd(self.bot.random.choice(cmds))


async def setup(bot):
    await bot.add_cog(Reactionbot(bot))
