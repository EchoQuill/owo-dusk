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
import threading
import time
import re
import os

from discord.ext import commands
from discord import DMChannel


with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

list_captcha = ["human", "captcha", "link", "letterword"]

def show_popup():
    messagebox.showinfo("OwO-Dusk notifier", "Captcha Detected!")

def clean(msg):
    return re.sub(r"[^a-zA-Z]", "", msg)

def is_termux():
    termux_prefix = os.environ.get("PREFIX")
    termux_home = os.environ.get("HOME")
    
    if termux_prefix and "com.termux" in termux_prefix:
        return True
    elif termux_home and "com.termux" in termux_home:
        return True
    else:
        return os.path.isdir("/data/data/com.termux")
    
on_mobile = is_termux()

if not on_mobile:
    #desktop
    from tkinter import messagebox
    from plyer import notification
    from playsound3 import playsound
    
def run_system_command(command, timeout, retry=False, delay=5):
    def target():
        try:
            os.system(command)
        except Exception as e:
            print(f"Error executing command: {command} - {e}")

    # Create and start a thread to execute the command
    thread = threading.Thread(target=target)
    thread.start()

    # Wait for the thread to finish, with a timeout
    thread.join(timeout)

    # If the thread is still alive after the timeout, terminate it
    if thread.is_alive():
        print(f"-error[0] {command} command failed!")
        if retry:
            print(f"-system[0] Retrying '{command}' after {delay}s")
            time.sleep(delay)
            run_system_command(command, timeout)

def get_channel_name(channel):
    if isinstance(channel, DMChannel):
        return "owo DMs"
    return channel.name

def console_handler(captcha=True):
    if config_dict["console"]["runConsoleCommandOnCaptcha"] and captcha:
        run_system_command(config_dict["console"]["commandToRunOnCaptcha"], timeout=5)
    elif config_dict["console"]["runConsoleCommandOnBan"] and not captcha:
        run_system_command(config_dict["console"]["commandToRunOnBan"], timeout=5)

def captcha_handler(channel, username, captcha_type):
    
    channel_name = get_channel_name(channel)
    content = 'captchaContent' if not captcha_type=="Ban" else 'bannedContent'
    """Notifications"""
    if config_dict["captcha"]["notifications"]["enabled"]:
        try:
            if on_mobile:
                run_system_command(
                    f"termux-notification -c '{config_dict['captcha']['notifications'][content].format(username=username,channelname=channel_name,captchatype=captcha_type)}'",
                    timeout=5, 
                    retry=True
                    )
            else:
                notification.notify(
                    title=f'{username} DETECTED CAPTCHA',
                    message=config_dict['captcha']['notifications'][content].format(username=username,channelname=channel_name,captchatype=captcha_type),
                    app_icon=None,
                    timeout=15
                    )
        except Exception as e:
            print(f"{e} - at notifs")
    """Play audio file"""
    """
    TASK: add two checks, check the path for the file in both outside utils folder
    and in owo-dusk folder
    +
    better error handling for missing PATH
    """
    if config_dict["captcha"]["playAudio"]["enabled"]:
        try:
            if on_mobile:
                run_system_command(f"termux-media-player play {config_dict['playAudio']['path']}", timeout=5, retry=True)
            else:
                playsound(config_dict["playAudio"]["path"], block=False)
        except Exception as e:
            print(f"{e} - at audio")
    """Toast/Popup"""
    if config_dict["captcha"]["toastOrPopup"]["enabled"]:
        try:
            if on_mobile:
                run_system_command(
                    f"termux-toast -c {config_dict['captcha']['toastOrPopup']['termuxToast']['textColour']} -b {config_dict['captcha']['toastOrPopup']['termuxToast']['backgroundColour']} '{config_dict['captcha']['toastOrPopup'][content].format(username=username,channelname=channel_name,captchatype=captcha_type)}'",
                    timeout=5,
                    retry=True
                    )
            else:
                pass
        except Exception as e:
            print(f"{e} - at Toast/Popup")
    """Termux - Vibrate"""
    if config_dict["captcha"]["termux"]["vibrate"]["enabled"]:
        try:
            if on_mobile:
                run_system_command(
                    f"termux-vibrate -f -d {config_dict['captcha']['termux']['vibrate']['time']*1000}",
                    timeout=5,
                    retry=True,
                )
            else:
                pass
        except Exception as e:
            print(f"{e} - at Toast/Popup")
    """Termux - TTS"""
    if config_dict["captcha"]["termux"]["textToSpeech"]["enabled"]:
        try:
            if on_mobile:
                run_system_command(
                        f"termux-tts-speak {config_dict['captcha']['termux']['textToSpeech'][content]}",
                        timeout=7,
                        retry=False
                    )
            else:
                pass
        except Exception as e:
            print(f"{e} - at Toast/Popup")

class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.dm.id and message.author.id == self.bot.owo_bot_id:
            if "I have verified that you are human! Thank you! :3" in message.content:
                self.bot.captcha = False
                self.bot.log(f"captcha solved! - {self.bot.user}", "chartreuse3")
                return

        if message.channel.id in {self.bot.dm.id, self.bot.cm.id} and message.author.id == self.bot.owo_bot_id:
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
                self.bot.log(f"captcha detected! - {self.bot.user}", "indian_red")
                captcha_handler(message.channel, self.bot.user, "Link")
                console_handler()

            elif "**☠ |** You have been banned" in message.content:
                self.bot.captcha = True
                captcha_handler(message.channel, self.bot.user, "Ban")
                console_handler(captcha=False)

            
        


async def setup(bot):
    await bot.add_cog(Captcha(bot))
