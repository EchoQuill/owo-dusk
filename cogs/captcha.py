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

import json
import re

from discord.ext import commands
from utils.captcha import captcha_handler # type: ignore


with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

list_captcha = ["human", "captcha", "link", "letterword"]


def clean(msg):
    return re.sub(r"[^a-zA-Z]", "", msg)


class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log("conf2 - captcha", "purple")

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.channel.id == self.bot.dm.id
            and message.author.id == self.bot.owo_bot_id
        ):
            if "I have verified that you are human! Thank you! :3" in message.content:
                self.bot.captcha = False
                self.bot.log(
                    f"captcha solved! - {self.bot.user}", "chartreuse3")

        if (
            message.channel.id in {self.bot.dm.id, self.bot.cm.id}
            and message.author.id == self.bot.owo_bot_id
        ):
            """sets may be faster than list..? maybe.."""
            if (
                (
                    message.components
                    and len(message.components) > 0
                    and hasattr(message.components[0], "children")
                    and len(message.components[0].children) > 0
                    and (
                        (
                            hasattr(message.components[0].children[0], "label")
                            and message.components[0].children[0].label == "Verify"
                        )
                        or (
                            hasattr(message.components[0].children[0], "url")
                            and message.components[0].children[0].url
                            == "https://owobot.com?login="
                        )
                    )
                )
                or (
                    "⚠️" in message.content and message.attachments
                )  # message attachment check
                or any(b in clean(message.content) for b in list_captcha)
            ):
                self.bot.captcha = True
                self.bot.log(
                    f"captcha detected! - {self.bot.user}", "indian_red")
                captcha_handler(message.channel, self.bot.user, "Link")


async def setup(bot):
    await bot.add_cog(Captcha(bot))
