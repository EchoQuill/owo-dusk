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


def find_least_gap(list_to_check):
    if len(list_to_check) < 2:
        return None

    final_result = {
        "min": list_to_check[0],
        "max": list_to_check[1],
        "diff": abs(list_to_check[1] - list_to_check[0]),
    }

    for i in range(len(list_to_check) - 1):
        curr = list_to_check[i]
        next_item = list_to_check[i + 1]
        diff = abs(next_item - curr)

        if diff < final_result["diff"]:
            final_result["min"] = curr
            final_result["max"] = next_item
            final_result["diff"] = diff if diff > 0 else 1

    return final_result


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd_tracker = []

    """def populate_cmd_tracker(self):
        # Reset cmd_tracker
        self.cmd_tracker = {}

        # populate
        for num, item in enumerate(self.bot.settings_dict["customCommands"]["commands"]):
            # Too lazy to handle irregularities caused by enable/disable
            # Lazy, but clean approach!
            self.cmd_tracker[num] = {
                "command": item["command"],
                "last_ran": 0
            }"""

    def approximate_minimum_cooldown(self):
        commands_dict = self.bot.settings_dict["customCommands"]["commands"]

        cooldowns_list = [
            item["cooldown"] for item in commands_dict if item.get("enabled")
        ]

        if not cooldowns_list:
            # just in case
            return 1

        # Sort in ascending order
        cooldowns_list = sorted(cooldowns_list)
        result = find_least_gap(cooldowns_list)

        if result:
            return min(result["diff"], min(cooldowns_list))
        else:
            return cooldowns_list[0]

    def search_cmd_tracker(self, cmd_dict):
        matches = []
        for idx, cmd_data in enumerate(self.cmd_tracker):
            if cmd_data["basedict"] == cmd_dict:
                matches.append({"index": idx, "data": cmd_data})

        return matches

    def fetch_last_ran_diff(self, last_ran, cooldown):
        # Checks if command can be ran or not.
        if last_ran != 0:
            cd = time.monotonic() - last_ran
            return {"required": cd > cooldown, "cooldown": cd}
        else:
            return {"required": False, "cooldown": 0}

    async def run_cmd(self, cmd_data, tracker_idx=None):
        cmd = {
            "cmd_name": cmd_data["command"],
            "prefix": False,
            "checks": False,
            "id": "customcommand",
            "removed": False,
        }

        await self.bot.put_queue(cmd)

        if tracker_idx is not None:
            self.cmd_tracker[tracker_idx]["last_ran"] = time.monotonic()
        else:
            self.cmd_tracker.append(
                {"basedict": cmd_data, "last_ran": time.monotonic()}
            )

    @tasks.loop()
    async def command_handler(self):
        cd = self.approximate_minimum_cooldown()
        cnf = self.bot.settings_dict["customCommands"]["commands"]
        for cmd_dict in cnf:
            if not cmd_dict["enabled"]:
                continue

            results = self.search_cmd_tracker(cmd_dict)
            if not results:
                await self.run_cmd(cmd_dict)
            else:
                cd_info_dict = self.fetch_last_ran_diff(
                    results[0]["data"]["last_ran"], cmd_dict["cooldown"]
                )
                if cd_info_dict["required"]:
                    await self.run_cmd(cmd_dict, results[0]["index"])

                if len(results) != 1:
                    # multiple data detected
                    pass

        await asyncio.sleep(cd)

    async def cog_load(self):
        if not self.bot.settings_dict["customCommands"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.customcommands"))
            except ExtensionNotLoaded:
                pass
        else:
            self.command_handler.start()

    async def cog_unload(self):
        self.command_handler.cancel()


async def setup(bot):
    await bot.add_cog(CustomCommands(bot))
