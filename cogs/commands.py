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
            print(list(self.bot.queue._queue))
            await self.bot.send(self.bot.construct_command(cmd))
            self.bot.log(f"Sent - {self.bot.construct_command(cmd)}", "#afafff")
            if cmd.get("checks"):
                async with self.bot.lock:
                    cmd["removed"] = cmd.get("removed", False)
                    self.bot.log(cmd, "#5f5f87")
                    self.bot.checks.append((cmd, datetime.now(timezone.utc)))
                    self.bot.log(f"{cmd}\n added to queue", "#5f5f87")
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
                async with self.bot.lock:
                    for index, (command, timestamp) in enumerate(self.bot.checks[:]):
                        if command.get("removed"):
                            self.bot.checks.remove((command, timestamp))
                            self.bot.log(f"removed {command} - monitor", "#5f5f87")
                            self.bot.log(self.bot.checks,"#5f5f87")
                            continue

                        if (current_time - timestamp).total_seconds() > 7:
                            await self.bot.put_queue(command)
                            print(f"put {command} to queue - monitor")
                            self.bot.checks[index] = (command, timestamp+timedelta(seconds=2))
                            #self.bot.checks.remove((command, timestamp))
            else:
                self.calc_time += current_time - getattr(self, "last_check_time", current_time)
            self.last_check_time = current_time
        except Exception as e:
            print(f"Error in monitor_checks: {e}")



async def setup(bot):
    await bot.add_cog(Commands(bot))