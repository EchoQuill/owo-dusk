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

from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta



class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.checks = []
        self.calc_time = timedelta(0)

    async def start_commands(self):
        await asyncio.sleep(self.bot.random_float(self.bot.config_dict["account"]["commandsHandlerStartDelay"]))
        await self.bot.shuffle_queue()
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
            if cmd.get("checks"):
                if cmd.get("id"):
                    in_queue = await self.bot.search_checks(id=cmd["id"])
                    if not in_queue:
                        async with self.bot.lock:
                            self.bot.checks.append((cmd, datetime.now(timezone.utc)))
            
            # Handle slash commands
            if self.bot.config_dict["useSlashCommands"] and cmd.get("slash_cmd_name", False):
                try:
                    # Pass additional parameters if available
                    kwargs = {}
                    if cmd.get("options"):
                        kwargs["options"] = cmd["options"]
                    if cmd.get("channel_id"):
                        kwargs["channel"] = self.bot.get_channel(cmd["channel_id"])
                    else:
                        kwargs["channel"] = self.bot.cm
                    
                    await self.bot.slashCommandSender(cmd["slash_cmd_name"], **kwargs)
                except Exception as e:
                    await self.bot.log(f"Error sending slash command {cmd['slash_cmd_name']}: {e}", "#FF0000")
                    # Try regular command as fallback if slash fails
                    if cmd.get("fallback_cmd"):
                        await self.bot.log(f"Trying fallback command", "#FFAA00")
                        await self.bot.send(self.bot.construct_command(cmd))
            else:
                # Regular command
                await self.bot.send(self.bot.construct_command(cmd))
                
            await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["commandHandler"]["betweenCommands"]))
        except Exception as e:
            print(f"Error in send_commands loop: {e}")
            await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["commandHandler"]["betweenCommands"]))

    @tasks.loop(seconds=1)
    async def monitor_checks(self):
        try:
            current_time = datetime.now(timezone.utc)
            if not self.bot.state or self.bot.sleep or self.bot.captcha:
                self.calc_time += current_time - getattr(self, "last_check_time", current_time)
            else:
                async with self.bot.lock:
                    for index, (command, timestamp) in enumerate(self.bot.checks[:]):
                        if command.get("removed"):
                            self.bot.checks.remove((command, timestamp))
                            continue
                        adjusted_time = timestamp + self.calc_time
                        if (current_time - adjusted_time).total_seconds() > self.bot.config_dict["defaultCooldowns"]["commandHandler"]["beforeReaddingToQueue"]:
                            await self.bot.put_queue(command)
                            self.bot.checks.remove((command, timestamp))
                self.calc_time = timedelta(0)
            self.last_check_time = current_time
        except Exception as e:
            print(f"Error in monitor_checks: {e}")




async def setup(bot):
    await bot.add_cog(Commands(bot))