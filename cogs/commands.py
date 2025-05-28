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

from collections import deque
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.checks = []
        self.calc_time = timedelta(0)
        self.command_times = deque(maxlen=3)
        


    
    def sleep_required(self):
        """makes sure three commands are within 5 second limit"""
        now = time.time()
        
        while self.command_times and now - self.command_times[0] >= 5:
            """Command has to be within 5 second limit"""
            self.command_times.popleft()
        
        if len(self.command_times) < 3:
            return False, 0
        else:
            wait_time = max(0, 5 - (now - self.command_times[0]))
            return True, wait_time
        
        

    async def start_commands(self):
        await self.bot.sleep_till(self.bot.global_settings_dict["account"]["commandsHandlerStartDelay"])
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
            cnf = self.bot.settings_dict["defaultCooldowns"]["commandHandler"]
            priority, _, cmd = await self.bot.queue.get()

            if priority != 0:
                while (time.time() - self.bot.cmds_state["global"]["last_ran"]) < cnf["betweenCommands"][0]:
                    await self.bot.sleep_till(cnf["betweenCommands"])

            sleep_req, sleep_time = self.sleep_required()
            if sleep_req:
                await self.bot.log(f"sleep required by {sleep_time}s", "#ffd359")
                await self.bot.sleep_till([sleep_time, sleep_time+0.4])
                self.command_times.clear()

            
            """Send the command"""
            await self.bot.upd_cmd_state(cmd["id"])
            
            if self.bot.settings_dict["useSlashCommands"] and cmd.get("slash_cmd_name", False):
                await self.bot.slashCommandSender(cmd["slash_cmd_name"])
            else:
                await self.bot.send(self.bot.construct_command(cmd))
            """add command to the deque"""
            self.command_times.append(time.time())
            
            """Append to checks"""
            if cmd.get("checks") and cmd.get("id"):
                in_queue = await self.bot.search_checks(id=cmd["id"])
                if not in_queue:
                    async with self.bot.lock:
                        #await self.bot.log(f"command {cmd} added to queue!", "#eeaaff")
                        self.bot.checks.append(cmd)

        except Exception as e:
            await self.bot.log(f"Error - send_commands() loop: {e}. {cmd.get('cmd_name', None)}", "#c25560")
            await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["commandHandler"]["betweenCommands"])

    @tasks.loop(seconds=1)
    async def monitor_checks(self):
        try:
            #await self.bot.log(f"started command monitor!", "#eeaaff")
            delay = self.bot.settings_dict["defaultCooldowns"]["commandHandler"]["beforeReaddingToQueue"]
            current_time = datetime.now(timezone.utc)
            if not self.bot.state or self.bot.sleep or self.bot.captcha:
                self.calc_time += current_time - getattr(self, "last_check_time", current_time)
            else:
                for command in self.bot.checks[:]:
                    #await self.bot.log(f"mon: {self.bot.checks[:]}", "#eeaaff")
                    cnf = self.bot.cmds_state[command["id"]]
                    #print(cnf, command["id"], cnf["last_ran"] - time.time(), cnf["last_ran"] - time.time() > delay)
                    if (time.time() - cnf["last_ran"] > delay) and not cnf["in_queue"]:
                        #await self.bot.log(f"{command['cmd_name']} has been readded to queue ({command['id']})", "#ffd359")
                        async with self.bot.lock:
                            self.bot.checks.remove(command)
                        await self.bot.put_queue(command)
                        #await self.bot.log(f"removed state: {self.bot.checks}", "#ffd359")


                self.calc_time = timedelta(0)
            self.last_check_time = current_time
        except Exception as e:
            await self.bot.log(f"Error - monitor_checks(): {e}", "#c25560")




async def setup(bot):
    await bot.add_cog(Commands(bot))