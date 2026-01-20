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

from discord.ext import commands
import asyncio
import json

import components_v2 as comp
from discord.ext.commands import ExtensionNotLoaded


class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boss_tickets = 3
        self.sleeping = True

    def should_join(self, percentage):
        boss_dict = self.bot.settings_dict["bossBattle"]
        random_num = self.bot.random.randint(1, 100)
        return random_num > (100 - boss_dict["joinChancePercent"])

    async def cog_load(self):
        if not self.bot.settings_dict["bossBattle"]["enabled"]:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.daily"))
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.time_check())

    async def wait_till_reset_day(self):
        self.sleeping = True
        time_to_sleep = self.bot.calc_time()
        await self.bot.log(f"Sleeping boss battle till {time_to_sleep}", "#143B02")
        await asyncio.sleep(time_to_sleep)
        await self.time_check()
        self.sleeping = False

    async def time_check(self):
        last_reset_ts, self.boss_tickets = await self.bot.fetch_boss_stats()

        today_midnight_ts = self.bot.pst_midnight_timestamp()

        if not last_reset_ts or last_reset_ts < today_midnight_ts:
            # Resetting incase new run or reset timing
            self.bot.reset_boss_ticket()
            self.boss_tickets = 3

            # update database
            self.bot.update_stats_db("boss", today_midnight_ts)

        self.sleeping = False

    def consume_boss_ticket(self):
        self.boss_tickets -= 1
        self.bot.consume_boss_ticket()

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        """
        https://discordpy-self.readthedocs.io/en/latest/api.html?highlight=on_socket_raw_receive#discord.on_socket_raw_receive
        For this to work enable_debug_events argument was passed as True in client.

        Right now we are getting the message object directly through on_socket_raw_receive
        we may want to consider getting message once and sharing them instead to reduce unneccesory parsing of raw input.
        """

        if self.boss_tickets <= 0 or self.sleeping:
            if not self.sleeping:
                await self.bot.log(
                    "Don't have enough boss tickets to join boss battle..", "#143B02"
                )
                await self.wait_till_reset_day()
            return

        parsed_msg = json.loads(msg)
        if parsed_msg["t"] != "MESSAGE_CREATE":
            return

        message = comp.message.get_message_obj(parsed_msg["d"])

        if (
            not self.bot.settings_dict["bossBattle"]["joinAllGuilds"]["enabled"]
            and message.channel_id != self.bot.cm.id
        ):
            return

        if message.author.id == self.bot.owo_bot_id:
            if message.components:
                for component in message.components:
                    # Boss Embed
                    if component.component_name == "section":
                        if (
                            component.component[0].content
                            and "runs away" in component.component[0].content
                        ):
                            if not self.should_join(
                                self.bot.settings_dict["bossBattle"][
                                    "joinChancePercent"
                                ]
                            ):
                                await self.bot.log("Skipping boss battle..", "#6F7C8A")
                                return

                            # Boss Fight button
                            if (
                                component.accessory
                                and component.accessory.component_name == "button"
                            ):
                                if component.accessory.custom_id == "guildboss_fight":
                                    boss_channel = await self.bot.fetch_channel(
                                        message.channel_id
                                    )

                                    if boss_channel:
                                        self.bot.boss_channel_id = boss_channel.id
                                        cnf = self.bot.settings_dict["bossBattle"][
                                            "joinAllGuilds"
                                        ]
                                        if (
                                            cnf["enabled"]
                                            and boss_channel.guild.id
                                            in cnf["guildIdsToIgnore"]
                                        ):
                                            # Skip incase in guild ignore list.
                                            return

                                        await asyncio.sleep(0.5)
                                        click_status = await component.accessory.click(
                                            self.bot.ws.session_id,
                                            self.bot.local_headers,
                                            boss_channel.guild.id,
                                        )
                                        if click_status:
                                            await self.bot.log(
                                                "Joined Boss battle!", "#B5C1CE"
                                            )

                    if component.component_name == "text_display":
                        if (
                            "Are you sure you want to use another boss ticket?"
                            in component.content
                        ):
                            await self.bot.log(
                                "Boss battle was already joined..", "#B5C1CE"
                            )
                            # redo changes made earlier..
                            self.bot.consume_boss_ticket(revert=True)
                            self.boss_tickets += 1

                        if "You don't have any boss tickets!" in component.content:
                            # Reset previous entry
                            self.boss_tickets = 0
                            self.bot.reset_boss_ticket(empty=True)


async def setup(bot):
    await bot.add_cog(Boss(bot))
