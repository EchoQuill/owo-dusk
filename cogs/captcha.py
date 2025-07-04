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

import threading
import time
import re
import os
import asyncio

from discord.ext import commands, tasks
from discord import DMChannel

list_captcha = ["human", "captcha", "link", "letterword"]

def get_path(path):
    cur_dir = os.getcwd()
    if os.path.isfile(path):
        """See if complete path"""
        return path
    audio_folder_path = os.path.join(cur_dir, "audio", path)
    if os.path.isfile(audio_folder_path):
        """See if audio file is in audio folder"""
        return audio_folder_path
    file_in_cwd = os.path.join(cur_dir, path)
    if os.path.isfile(file_in_cwd):
        """See if audio file is in working directory"""
        return file_in_cwd
    """None otherwise"""
    return None



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
        print(f"Error: {command} command failed! (captcha)")
        if retry:
            print(f"Retrying '{command}' after {delay}s")
            time.sleep(delay)
            run_system_command(command, timeout)

def get_channel_name(channel):
    if isinstance(channel, DMChannel):
        return "owo DMs"
    return channel.name

def console_handler(cnf, captcha=True):
    if cnf["runConsoleCommandOnCaptcha"] and captcha:
        run_system_command(cnf["commandToRunOnCaptcha"], timeout=5)
    elif cnf["runConsoleCommandOnBan"] and not captcha:
        run_system_command(cnf["commandToRunOnBan"], timeout=5)


class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def captcha_handler(self, channel, captcha_type):
        if self.bot.misc["hostMode"]:
            return
        cnf = self.bot.global_settings_dict["captcha"]
        channel_name = get_channel_name(channel)
        content = 'captchaContent' if not captcha_type=="Ban" else 'bannedContent'
        """Notifications"""
        if cnf["notifications"]["enabled"]:
            try:
                if on_mobile:
                    run_system_command(
                        f"termux-notification -t '{self.bot.username} captcha!' -c '{cnf['notifications'][content].format(username=self.bot.username,channelname=channel_name,captchatype=captcha_type)}' --led-color '#a575ff' --priority 'high'",
                        timeout=5, 
                        retry=True
                        )
                else:
                    notification.notify(
                        title=f'{self.bot.username} DETECTED CAPTCHA',
                        message=cnf['notifications'][content].format(username=self.bot.username,channelname=channel_name,captchatype=captcha_type),
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
        if cnf["playAudio"]["enabled"]:
            path = get_path(cnf['playAudio']['path'])
            try:
                if on_mobile:
                    run_system_command(f"termux-media-player play {path}", timeout=5, retry=True)
                else:
                    playsound(path, block=False)
            except Exception as e:
                print(f"{e} - at audio")
        """Toast/Popup"""
        if cnf["toastOrPopup"]["enabled"]:
            try:
                if on_mobile:
                    run_system_command(
                        f"termux-toast -c {cnf['toastOrPopup']['termuxToast']['textColour']} -b {cnf['toastOrPopup']['termuxToast']['backgroundColour']} -g {cnf['toastOrPopup']['termuxToast']['position']} '{cnf['toastOrPopup'][content].format(username=self.bot.username,channelname=channel_name,captchatype=captcha_type)}'",
                        timeout=5,
                        retry=True
                        )
                else:
                    self.bot.add_popup_queue(channel_name, captcha_type)
            except Exception as e:
                print(f"{e} - at Toast/Popup")
        """Termux - Vibrate"""
        if cnf["termux"]["vibrate"]["enabled"]:
            try:
                if on_mobile:
                    run_system_command(
                        f"termux-vibrate -f -d {cnf['termux']['vibrate']['time']*1000}",
                        timeout=5,
                        retry=True,
                    )
                else:
                    pass
            except Exception as e:
                print(f"{e} - at Toast/Popup")
        """Termux - TTS"""
        if cnf["termux"]["textToSpeech"]["enabled"]:
            try:
                if on_mobile:
                    run_system_command(
                            f"termux-tts-speak {cnf['termux']['textToSpeech'][content]}",
                            timeout=7,
                            retry=False
                        )
                else:
                    pass
            except Exception as e:
                print(f"{e} - at Toast/Popup")
        """Termux - open captcha website"""
        if cnf["termux"]["openCaptchaWebsite"] and on_mobile:
            run_system_command("termux-open https://owobot.com/captcha", timeout=5, retry=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        self.last_msg = time.time()

        if not self.bot.dm:
            if message.author.id == self.bot.owo_bot_id:
                self.bot.dm = await message.author.create_dm()
            else:
                # Safe, since only owobot will send captcha messages.
                return


        if message.channel.id == self.bot.dm.id and message.author.id == self.bot.owo_bot_id:
            if "I have verified that you are human! Thank you! :3" in message.content:
                time_to_sleep = self.bot.random_float(self.bot.settings_dict['defaultCooldowns']['captchaRestart'])
                await self.bot.log(f"Captcha solved! - sleeping {time_to_sleep}s before restart.", "#5fd700")
                await asyncio.sleep(time_to_sleep)
                self.bot.command_handler_status["captcha"] = False
                await self.bot.update_captcha_db()
                return

        if message.channel.id in {self.bot.dm.id, self.bot.cm.id} and message.author.id == self.bot.owo_bot_id:
            """Handle normally expected captcha"""
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
                if not get_channel_name(message.channel) == "owo DMs":
                    display_name = message.guild.me.display_name
                    if not any(user in message.content for user in (self.bot.user.name, f"<@{self.bot.user.id}>", display_name)):
                        return
                self.bot.command_handler_status["captcha"] = True
                await self.bot.log(f"Captcha detected!", "#d70000")
                self.captcha_handler(message.channel, "Link")
                if self.bot.global_settings_dict["webhook"]["enabled"]:
                    await self.bot.webhookSender(
                        msg=f"-{self.bot.username} [+] CAPTCHA Detected",
                        desc=f"**User** : <@{self.bot.user.id}>\n**Link** : [OwO Captcha]({message.jump_url})",
                        colors="#00FFAF",
                        img_url="https://cdn.discordapp.com/emojis/1171297031772438618.png",
                        author_img_url="https://i.imgur.com/6zeCgXo.png",
                        plain_text=(
                            f"<@{self.bot.global_settings_dict['webhook']['webhookUserIdToPingOnCaptcha']}>"
                            if self.bot.global_settings_dict['webhook']['webhookUserIdToPingOnCaptcha']
                            else None
                        ),
                        webhook_url=self.bot.global_settings_dict["webhook"].get("webhookCaptchaUrl", None),
                    )
                console_handler(self.bot.global_settings_dict["console"])

            elif "**☠ |** You have been banned" in message.content:
                self.bot.command_handler_status["captcha"] = True
                await self.bot.log(f"Ban detected!", "#d70000")
                self.captcha_handler(message.channel, "Ban")
                console_handler(self.bot.global_settings_dict["console"], captcha=False)
                if self.bot.global_settings_dict["webhook"]["enabled"]:
                    await self.bot.webhookSender(
                        msg=f"-{self.bot.username} [+] BAN Detected",
                        desc=f"**User** : <@{self.bot.user.id}>\n**Link** : [Ban Message]({message.jump_url})",
                        colors="#00FFAF",
                        img_url="https://cdn.discordapp.com/emojis/1213902052879503480.gif",
                        author_img_url="https://i.imgur.com/6zeCgXo.png",
                        plain_text=(
                            f"<@{self.bot.global_settings_dict['webhook']['webhookUserIdToPingOnCaptcha']}>"
                            if self.bot.global_settings_dict["webhook"]["webhookUserIdToPingOnCaptcha"]
                            else None
                        ),
                        webhook_url=self.bot.global_settings_dict["webhook"].get("webhookCaptchaUrl", None),
                    )
            elif message.embeds:
                for embed in message.embeds:
                    items = {
                        embed.title if embed.title else "",
                        embed.author.name if embed.author else "",
                        embed.footer.text if embed.footer else "",
                    }
                    for i in items:
                        if any(b in clean(i) for b in list_captcha):
                            """clean function cleans the captcha message of unwanted symbols etc"""
                            self.bot.command_handler_status["captcha"] = True
                            await self.bot.log(f"Captcha detected...?", "#d70000")
                            break

                    if embed.fields:
                        for field in embed.fields:
                            if field.name and any(b in clean(field.name) for b in list_captcha):
                                self.bot.command_handler_status["captcha"] = True
                                await self.bot.log(f"Captcha detected...?", "#d70000")
                                break
                            if field.value and any(b in clean(field.value) for b in list_captcha):
                                self.bot.command_handler_status["captcha"] = True
                                await self.bot.log(f"Captcha detected...?", "#d70000")
                                break

async def setup(bot):
    await bot.add_cog(Captcha(bot))
