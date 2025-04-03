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
from datetime import datetime, timezone, timedelta




class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.checks = []
        self.calc_time = timedelta(0)
        self.retry_spam_count = 0
        self.last_retry = 0
        

    async def start_commands(self):
        await self.bot.sleep_till(self.bot.config_dict["account"]["commandsHandlerStartDelay"])
        await self.bot.shuffle_queue()
        self.send_commands.start()
        self.monitor_checks.start()

    async def cog_load(self):
        """Run join_previous_giveaways when bot is ready"""
        asyncio.create_task(self.start_commands())

    
    def fetch_delay(self):
        cnf = self.bot.config_dict["defaultCooldowns"]["commandHandler"]["beforeReaddingToQueue"]
        delay = min(cnf["baseDelay"] * (2 ** self.retry_spam_count), cnf["maxDelay"])
        return delay
    
    """send commands"""
    @tasks.loop()
    async def send_commands(self):
        try:
            cmd = await self.bot.queue.get()
            await self.bot.log(f"current command {cmd['cmd_name']}, with id {cmd.get('id', 'none')}", "#ffd359")
            await self.bot.log(f"current list: {self.bot.queue._queue}", "#ffd359")
            if cmd.get("checks") and cmd.get("id"):
                in_queue = await self.bot.search_checks(id=cmd["id"])
                if not in_queue:
                    async with self.bot.lock:
                        self.bot.checks.append((cmd, datetime.now(timezone.utc)))
            if self.bot.config_dict["useSlashCommands"] and cmd.get("slash_cmd_name", False):
                await self.bot.slashCommandSender(cmd["slash_cmd_name"])
                await self.bot.upd_cmd_time()
            else:
                await self.bot.send(self.bot.construct_command(cmd))
                await self.bot.upd_cmd_time()
            while (time.time() - self.bot.last_cmd_ran) < self.bot.config_dict["defaultCooldowns"]["commandHandler"]["betweenCommands"][0]:
                await self.bot.sleep_till(self.bot.config_dict["defaultCooldowns"]["commandHandler"]["betweenCommands"])
        except Exception as e:
            print(f"Error in send_commands loop: {e}")
            await self.bot.sleep_till(self.bot.config_dict["defaultCooldowns"]["commandHandler"]["betweenCommands"])

    @tasks.loop(seconds=1)
    async def monitor_checks(self):
        try:
            #print(f"current monitor: {self.bot.checks}")
            cnf = self.bot.config_dict["defaultCooldowns"]["commandHandler"]
            delay = self.fetch_delay()
            current_time = datetime.now(timezone.utc)
            if not self.bot.state or self.bot.sleep or self.bot.captcha:
                self.calc_time += current_time - getattr(self, "last_check_time", current_time)
            else:
                async with self.bot.lock:
                    for index, (command, timestamp) in enumerate(self.bot.checks[:]):
                        adjusted_time = timestamp + self.calc_time
                        if (current_time - adjusted_time).total_seconds() > delay:
                            await self.bot.log(f"{command['cmd_name']} has been readded to queue ({command['id']})", "#ffd359")
                            self.bot.checks.remove((command, timestamp))
                            await self.bot.put_queue(command)
                            await self.bot.log(f"removed state: {self.bot.checks}", "#ffd359")
                            
                            temp_time = time.time()
                            if (temp_time - self.last_retry) > cnf["beforeReaddingToQueue"]["antiSpamThreshold"]:
                                self.retry_spam_count = 0
                            else:
                                self.retry_spam_count += 1
                            self.last_retry = temp_time


                self.calc_time = timedelta(0)
            self.last_check_time = current_time
        except Exception as e:
            print(f"Error in monitor_checks: {e}")




async def setup(bot):
    await bot.add_cog(Commands(bot))