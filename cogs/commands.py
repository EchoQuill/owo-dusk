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

from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta



class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.checks = []
        self.calc_time = timedelta(0)

    async def start_commands(self):
        await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["briefCooldown"]))
        self.send_commands.start()
        self.monitor_checks.start()

    async def cog_load(self):
        """Run join_previous_giveaways when bot is ready"""
        asyncio.create_task(self.start_commands())
    
    """send commands"""
    @tasks.loop()
    async def send_commands(self):
        try:
            cmd = await self.bot.queue.get()
            await self.bot.send(self.bot.construct_command(cmd))
            if cmd.get("checks") and not cmd.get("removed", False):
                self.bot.checks.append((cmd, datetime.now(timezone.utc)))
            await asyncio.sleep(random.uniform(0.7, 1.2))
        except Exception as e:
            print(f"Error in send_commands loop: {e}")
            await asyncio.sleep(random.uniform(0.7, 1.2))

    """TASK: check monitor"""

    @tasks.loop(seconds=1)
    async def monitor_checks(self):
        try:
            current_time = datetime.now(timezone.utc)
            if not self.bot.captcha and self.bot.state:
                for command, timestamp in self.bot.checks[:]:  # Work on a copy to avoid issues
                    if command.get("removed"):  # Skip if marked as removed
                        self.bot.log(f"Skipping removed command: {command}", "yellow")
                        self.bot.checks.remove((command, timestamp))  # Remove it permanently
                        continue

                    if (current_time - timestamp).total_seconds() > 7:
                        await self.bot.put_queue(command)
                        self.bot.log(f"Added {command} back to queue", "cornflower_blue")
                        self.bot.checks.remove((command, timestamp))  # Remove processed command
            else:
                self.calc_time += current_time - getattr(self, "last_check_time", current_time)
            self.last_check_time = current_time
        except Exception as e:
            print(f"Error in monitor_checks: {e}")



async def setup(bot):
    await bot.add_cog(Commands(bot))