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

        self.last_msg = 0


    @tasks.loop()
    async def watchdog(self):
        # Watch dog for unresponsive code
        # added mostly due to library issues cause code to be unresponsive
        # incase code becomes unresponsive we will attempt a retry

        cd = await self.min_seconds_for_watchdog()

        if cd is None:
            self.watchdog.cancel()
            return

        await asyncio.sleep(cd)
        

        if time.time() - self.last_msg >= cd:
            await self.bot.log(f"UNABLE TO DETECT MESSAGES!", "#8b1657")
            self.bot.command_handler_status["captcha"] = True # Prevent any further messages
            await self.bot.log(f"Code was stopped for obvious reasons, please report logs of when this happened along with any errors to @echoquill\nYou may report through either dms or support server!", "#8b1657")

            print("attempting to trigger retry!")
            await self.bot.close()

    async def min_seconds_for_watchdog(self):
        req = 1000
        cnf = self.bot.settings_dict["commands"]
        for cmd in cnf.values():
            if cmd["enabled"]:
                if cmd.get("cooldown"):
                    cd = cmd["cooldown"][0]
                    req = cd if cd < req else req

        if req != 1000:
            threshold = req+10
        else:
            await self.bot.log(f"Disabling watchdog since no valid cooldown found", "#13353a")
            # Rest would daily, cookie etc which doesnt really cause much issues even in case of failure.
            # It would be safe to assume nothing wrong will happen (hopefully)
            return None
        #await self.bot.log(f"Watchdog threshold: {threshold}s", "#13353a")
        return threshold

        

    
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
        #self.watchdog.start()

    async def cog_load(self):
        """Run join_previous_giveaways when bot is ready"""
        asyncio.create_task(self.start_commands())
    
    """send commands"""
    @tasks.loop()
    async def send_commands(self):
        try:
            cnf = self.bot.settings_dict["defaultCooldowns"]["commandHandler"]
            priority, _, cmd = await self.bot.queue.get()
            cmd_id = cmd.get("id")

            if priority != 0:
                while (time.time() - self.bot.cmds_state["global"]["last_ran"]) < cnf["betweenCommands"][0]:
                    await self.bot.sleep_till(cnf["betweenCommands"])

            sleep_req, sleep_time = self.sleep_required()
            if sleep_req:
                await self.bot.log(f"sleep required by {sleep_time}s (to prevent `slow down` message)", "#8f6b09")
                await self.bot.sleep_till([sleep_time, sleep_time+0.4])
                self.command_times.clear()

            
            """Update Command state"""
            await self.bot.upd_cmd_state(cmd_id)

            """Append to checks"""
            if cmd.get("checks") and cmd_id:
                in_queue = await self.bot.search_checks(id=cmd_id)
                if not in_queue:
                    async with self.bot.lock:
                        self.bot.checks.append(cmd)
            
            if self.bot.settings_dict["useSlashCommands"] and cmd.get("slash_cmd_name", False):
                await self.bot.slashCommandSender(cmd["slash_cmd_name"], self.bot.misc["command_info"][cmd_id]["log_color"])
            else:
                await self.bot.send(self.bot.construct_command(cmd), self.bot.misc["command_info"][cmd_id]["log_color"])

            """add command to the deque"""
            self.command_times.append(time.time())
            

        except Exception as e:
            await self.bot.log(f"Error - send_commands() loop: {e}. {cmd.get('cmd_name', None)}", "#c25560")
            await self.bot.sleep_till(self.bot.settings_dict["defaultCooldowns"]["commandHandler"]["betweenCommands"])

    @tasks.loop(seconds=1)
    async def monitor_checks(self):
        try:
            delay = self.bot.settings_dict["defaultCooldowns"]["commandHandler"]["beforeReaddingToQueue"]
            current_time = datetime.now(timezone.utc)
            if not self.bot.command_handler_status["state"] or self.bot.command_handler_status["sleep"] or self.bot.command_handler_status["captcha"]:
                self.calc_time += current_time - getattr(self, "last_check_time", current_time)
            else:
                for command in self.bot.checks[:]:
                    cnf = self.bot.cmds_state[command["id"]]
                    if (time.time() - cnf["last_ran"] > delay) and not cnf["in_queue"]:
                        async with self.bot.lock:
                            self.bot.checks.remove(command)
                        await self.bot.put_queue(command)


                self.calc_time = timedelta(0)
            self.last_check_time = current_time
        except Exception as e:
            await self.bot.log(f"Error - monitor_checks(): {e}", "#c25560")

    """@commands.Cog.listener()
    async def on_message(self, message):
        self.last_msg = time.time()"""




async def setup(bot):
    await bot.add_cog(Commands(bot))