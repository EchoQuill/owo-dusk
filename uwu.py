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


from datetime import datetime, timedelta, timezone
from discord.ext import commands
from rich.console import Console
from threading import Thread
from rich.panel import Panel
from rich.align import Align
from datetime import datetime
import discord
import asyncio
import logging
import random
import traceback
import subprocess
import threading
import aiohttp
import json
import pytz
import sys
import os
import time
import requests


def clear():
    os.system('cls') if os.name == 'nt' else os.system('clear')

console = Console()
lock = threading.Lock()
clear()

def load_accounts_dict(file_path="utils/stats.json"):
    with open(file_path, "r") as config_file:
        return json.load(config_file)

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)



console.rule("[bold blue1]:>", style="navy_blue")
console_width = console.size.width
listUserIds = []

owo_dusk_api = "https://echoquill.github.io/owo-dusk-api"

owoArt = r"""
  __   _  _   __       ____  _  _  ____  __ _ 
 /  \ / )( \ /  \  ___(    \/ )( \/ ___)(  / )
(  O )\ /\ /(  O )(___)) D () \/ (\___ \ )  ( 
 \__/ (_/\_) \__/     (____/\____/(____/(__\_)
"""
owoPanel = Panel(Align.center(owoArt), style="purple on black", highlight=False)
version = "2.0.0-alpha"
debug_print = True

def printBox(text, color, title=None):
    test_panel = Panel(text, style=color, title=title)
    console.print(test_panel)

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def try_import_or_install(package_name):
    try:
        __import__(package_name)
        print(f"Module {package_name} imported successfully.")
    except ImportError:
        print(f"{package_name} is not installed, attempting to install automatically...")
        try:
            install_package(package_name)
            __import__(package_name)
            print(f"{package_name} installed and imported successfully.")
        except Exception as e:
            print(f"Failed to install {package_name}. Please run 'pip install {package_name}' and run the script again. Error: {e}")

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
    try_import_or_install("psutil")
    try:
        import psutil

        print("psutil imported successfully")
    except Exception as e:
        print(f"ImportError: {e}")


# For battery check
def batteryCheckFunc():
    try:
        if on_mobile:
            while True:
                time.sleep(config_dict["batteryCheck"]["refreshInterval"])
                try:
                    battery_status = os.popen("termux-battery-status").read()
                except Exception as e:
                    console.print(
                        f"""-system[0] Battery check failed!!""".center(console_width - 2),
                        style="red on black",
                    )
                battery_data = json.loads(battery_status)
                percentage = battery_data["percentage"]
                console.print(
                    f"-system[0] Current battery •> {percentage}".center(console_width - 2),
                    style="blue on black",
                )
                if percentage < int(config_dict["batteryCheck"]["minPercentage"]):
                    break
        else:
            while True:
                time.sleep(config_dict["batteryCheck"]["refreshInterval"])
                try:
                    battery = psutil.sensors_battery()
                    if battery is not None:
                        percentage = int(battery.percent)
                        console.print(
                            f"-system[0] Current battery •> {percentage}".center(console_width - 2),
                            style="blue on black",
                        )
                        if percentage < int(config_dict["batteryCheck"]["minPercentage"]):
                            break
                except Exception as e:
                    console.print(
                        f"""-system[0] Battery check failed!!.""".center(console_width - 2),
                        style="red on black",
                    )
    except Exception as e:
        print("battery check", e)
    os._exit(0)

if config_dict["batteryCheck"]["enabled"]:
    loop_thread = threading.Thread(target=batteryCheckFunc)
    loop_thread.start()

class MyClient(commands.Bot):
    
    def __init__(self, token, channel_id, *args, **kwargs):
        """The self_bot here makes sure the inbuild command `help`
        doesn't get executed by other users."""
        
        super().__init__(command_prefix="-", self_bot=True, *args, **kwargs)
        self.token = token
        self.channel_id = int(channel_id)
        self.list_channel = [self.channel_id]
        self.session = None
        """`self.state` will be used to stop code for general stuff like for commands etc
        and `self.captcha` for captchas to prevent anything unexpected causing the code to run
        even after captcha..."""
        self.state = True
        self.captcha = False
        self.balance = 0
        self.queue = asyncio.Queue()
        self.config_dict = None
        self.update_config()



    """Update config.json"""
    def update_config(self):
        with open("config.json", "r") as config_file:
            # Read the JSON data directly
            self.config_dict = json.load(config_file)

    async def unload_cog(self, cog_name):
        try:
            await self.unload_extension(cog_name)
        except Exception as e:
            print(e)
        
    """To make the code cleaner when accessing cooldowns from config."""
    def random_float(self, cooldown_list):
        return random.uniform(cooldown_list[0],cooldown_list[1])
    
    """
    DATA EXAMPLE:
    command_data = {
        "cmd_name": "sell",
        "cmd_arguments": rarity_value,
        "prefix": True,
        "checks": True,
        "retry_count": 0
}
    """
    
    def construct_command(self, data):
        prefix = config_dict['setprefix'] if data.get("prefix") else ""
        return f"{prefix}{data['cmd_name']} {data.get('cmd_arguments', '')}".strip()


    async def put_queue(self, cmd_data, priority=False):
        try:
            while not self.state or self.captcha:
                if priority:
                    await self.queue.put(cmd_data)
                    return
                await asyncio.sleep(random.uniform(1.4,2.9))
            await self.queue.put(cmd_data)
        except Exception as e:
            print(e)
            print("^ at put_queue")
    
    def remove_queue(self, cmd_data, **kwargs):
        try:
            self.checks = [
                check for check in self.checks 
                if check[0] != cmd_data
            ]
        except Exception as e:
            print(e)
            print("^ at remove_queue")



    def log(self, text, color, bold=False, debug=config_dict["debug"]["enabled"], save_log=config_dict["debug"]["logInTextFile"]):
        style = f"{color} on black"
        if debug:
            # Get the stack trace and the caller frame info
            frame_info = traceback.extract_stack()[-2]
            filename = os.path.basename(frame_info.filename)
            lineno = frame_info.lineno
            current_time = datetime.now().strftime("%H:%M:%S")
            content_to_print = f"[{current_time}] {text} | [{filename}:{lineno}]"
            console.print(content_to_print, style=style, markup=False)
            if save_log:
                with open("logs.txt", "a") as log:  # Open in append mode
                    log.write(f"{text}\n")

        else:
            console.print(text.center(console_width - 2), style=style)



    # send commands
    async def send(self, message, bypass=False, channel=None, slash_command=False, slash_command_arg=None, silent=config_dict["silentTextMessages"], typingIndicator=config_dict["typingIndicator"]):
        if not channel:
            channel = self.cm
        if not self.captcha or bypass:
            if typingIndicator:
                async with channel.typing():
                    await channel.send(message, silent=silent)
                    if slash_command:
                        self.slashCommandSender(message)
            else:
                await channel.send(message, silent=silent)
                if slash_command:
                    self.slashCommandSender(message)
    async def slashCommandSender(self, msg, **kwargs):
        try:
            for command in self.commands:
                if command.name == msg:
                    await command(**kwargs)
        except Exception as e:
            print(e)

    def calc_time(self):
        pst_timezone = pytz.timezone('US/Pacific') #gets timezone
        current_time_pst = datetime.now(timezone.utc).astimezone(pst_timezone) #current pst time
        midnight_pst = pst_timezone.localize(datetime(current_time_pst.year, current_time_pst.month, current_time_pst.day, 0, 0, 0)) #gets 00:00 of the day
        time_until_12am_pst = midnight_pst + timedelta(days=1) - current_time_pst # adds a day to the midnight to get time till next midnight, then subract it with current time
        total_seconds = time_until_12am_pst.total_seconds() # turn that time to seconds
        # 12am = 00:00, I might need this the next time I take a look here.
        return total_seconds

    async def on_ready(self):
        #self.on_ready_dn = False
        self.owo_bot_id = 408785106942164992
        if self.session is None:
            self.session = aiohttp.ClientSession()
        await asyncio.sleep(self.random_float(config_dict["account"]["startupDelay"]))
        printBox(f'-Loaded {self.user.name}[*].'.center(console_width - 2 ),'bold royal_blue1 on black' )
        listUserIds.append(self.user.id)

        try:
            self.cm = self.get_channel(self.channel_id)
        except Exception as e:
            print(e)
        """
        NOTE:- Temporary fix for https://github.com/dolfies/discord.py-self/issues/744
        Hopefully the above gets fixed soon.
        for now we will send `owo ping` command in the grind channel to get owo bot's message through the channels history.
        then we will use that instead to create the dm
        """
        try:
            self.dm = await (self.get_user(self.owo_bot_id)).create_dm()
            if self.dm == None:
                self.dm = await (self.fetch_user(self.owo_bot_id)).create_dm()
        except discord.Forbidden as e:
            print(e)
            print(f"attempting to get user with the help of {self.cm}")
            await self.cm.send(f"{config_dict['setprefix']}ping")
            async for message in self.cm.history(limit=10):
                if message.author.id == self.owo_bot_id:
                    break
            await asyncio.sleep(random.uniform(0.5,0.9))
            self.dm = await message.author.create_dm()
        except Exception as e:
            print(e)

        """Fetch slash commands in self.cm"""
        self.slash_commands = []
        for command in await self.cm.application_commands():
            if command.application.id == 408785106942164992:
                self.slash_commands.append(command)

        """add account to stat.json"""
        self.default_config = {
            self.user.id: {
                "daily": 0,
                "lottery": 0,
                "cookie": 0,
                "banned": [],
                "giveaways": 0
            }
        }
        with lock:
            accounts_dict = load_accounts_dict()
            if str(self.user.id) not in accounts_dict:
                accounts_dict.update(self.default_config)
                with open("utils/stats.json", "w") as f:
                    json.dump(accounts_dict, f, indent=4)
                accounts_dict = load_accounts_dict()

                print(f"Default values added for bot ID: {self.user.id}")

        # Load cogs
        for filename in os.listdir(resource_path("./cogs")):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                #print(filename)
        #self.log(f'{self.user}[+] ran hunt', 'purple')

        

#----------STARTING BOT----------#                 
def run_bots(tokens_and_channels):
    threads = []
    for token, channel_id in tokens_and_channels:
        thread = Thread(target=run_bot, args=(token, channel_id))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
def run_bot(token, channel_id):
    logging.getLogger("discord.client").setLevel(logging.ERROR)
    client = MyClient(token, channel_id)
    client.run(token, log_level=logging.ERROR)
if __name__ == "__main__":
    console.print(owoPanel)
    console.rule(f"[bold blue1]version - {version}", style="navy_blue")
    printBox(f'-Made by EchoQuill'.center(console_width - 2 ),'bold grey30 on black' )
    #printBox(f'-Current Version:- {version}'.center(console_width - 2 ),'bold spring_green4 on black' )
    tokens_and_channels = [line.strip().split() for line in open("tokens.txt", "r")]
    token_len = len(tokens_and_channels)
    printBox(f'-Recieved {token_len} tokens.'.center(console_width - 2 ),'bold magenta on black' )
    try:
        news_json = requests.get(f"{owo_dusk_api}/news.json").json()
        if news_json["available"]:
            printBox(f'{news_json["content"]}'.center(console_width - 2 ),'bold aquamarine1 on black', title=news_json["title"] )
    except Exception as e:
        print(e)
    console.print("Star the repo in our github page if you want us to continue maintaining this proj :>.", style = "thistle1 on black")
    console.rule(style="navy_blue")
    run_bots(tokens_and_channels)
