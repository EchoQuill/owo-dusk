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


"""
fix pray.curse
fix commands disabled not stopping
add gamble, shop blah blah
recolour, if possible rename!
"""

from datetime import datetime, timedelta, timezone
from discord.ext import commands, tasks
from rich.console import Console
from threading import Thread
from rich.panel import Panel
from rich.align import Align
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import json
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
owoPanel = Panel(Align.center(owoArt), style="purple ", highlight=False)
version = "2.0.0-alpha"
debug_print = True



"""FLASK APP"""

app = Flask(__name__)
website_logs = []
config_updated = False

def merge_dicts(main, small):
    for key, value in small.items():
        if key in main and isinstance(main[key], dict) and isinstance(value, dict):
            merge_dicts(main[key], value)
        else:
            main[key] = value

@app.route("/")
def home():
    return render_template("index.html", version=version)


@app.route("/api/saveThings", methods=["POST"])
def save_things():
    global config_updated
    try:
        data = request.get_json()
        print(data)
        if not data:
            return jsonify({"status": "error", "message": "Invalid or missing JSON data"}), 400
        with open("config.json", "r") as main_config:
            main_data = json.load(main_config)
        merge_dicts(main_data, data)
        with open("config.json", "w") as main_config:
            json.dump(main_data, main_config, indent=4)
        print('saved successfully!')
        config_updated = True

        return jsonify({"status": "success", "message": "Data received and saved successfully"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "An error occurred while saving data"}), 500
    
@app.route('/api/config', methods=['GET'])
def get_config():
    # Check for 'password' in the headers
    password = request.headers.get('password')
    if not password or password != "password":  # Replace "expected_password" with your actual check
        return jsonify({"error": "Unauthorized"}), 401
    with open("config.json", "r") as file:
        config_data = json.load(file)
    # Return the configuration data as JSON
    return jsonify(config_data)


@app.route('/api/console', methods=['GET'])
def get_console_logs():
    try:
        
        # Join logs with newline character to make it similar to JS response
        log_string = '\n'.join(website_logs)
        
        return log_string  # Send logs as plain text response
        
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return jsonify({"status": "error", "message": "An error occurred while fetching logs"}), 500
    

def web_start():
    flaskLog = logging.getLogger("werkzeug")
    flaskLog.disabled = True
    cli = sys.modules["flask.cli"]
    cli.show_server_banner = lambda *x: None
    try:
        app.run(debug=False, use_reloader=False, port=config_dict["website"]["port"])
    except Exception as e:
        print(e)
if config_dict["website"]["enabled"]:
    try:
        web_thread = threading.Thread(target=web_start)
        web_thread.start()
    except Exception as e:
        print(e)

""""""

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
                        style="red ",
                    )
                battery_data = json.loads(battery_status)
                percentage = battery_data["percentage"]
                console.print(
                    f"-system[0] Current battery •> {percentage}".center(console_width - 2),
                    style="blue ",
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
                            style="blue ",
                        )
                        if percentage < int(config_dict["batteryCheck"]["minPercentage"]):
                            break
                except Exception as e:
                    console.print(
                        f"""-system[0] Battery check failed!!.""".center(console_width - 2),
                        style="red ",
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
        self.commands_dict = {}
        self.lock = asyncio.Lock()

    @tasks.loop(seconds=5)
    async def config_update_checker(self):
        global config_updated
        if config_updated:
            await self.update_config()
            config_updated = False


    async def start_cogs(self):
        for filename in os.listdir(resource_path("./cogs")):
            if filename.endswith(".py"):
                extension = f"cogs.{filename[:-3]}"
                if extension in self.extensions:
                    """skip if already loaded"""
                    self.refresh_commands_dict()
                    if not self.commands_dict[str(filename[:-3])]:
                        await self.unload_cog(extension)
                        print(f"disabled {extension}")
                    continue
                try:
                    await self.load_extension(extension)
                    print(f"Loaded extension: {extension}")
                except Exception as e:
                    print(f"Failed to load extension {extension}: {e}")

    async def update_config(self):
        print("task received")

        with open("config.json", "r") as config_file:
            self.config_dict = json.load(config_file)

        await self.start_cogs()

    async def unload_cog(self, cog_name):
        try:
            await self.unload_extension(cog_name)
        except Exception as e:
            print(e)

    def refresh_commands_dict(self):
        self.commands_dict = {
            "battle": self.config_dict["commands"]["battle"]["enabled"],
            "captcha": True,
            "coinflip": self.config_dict["gamble"]["coinflip"]["enabled"],
            "commands": True,
            "cookie": self.config_dict["commands"]["cookie"]["enabled"],
            "daily": self.config_dict["autoDaily"],
            "gems": self.config_dict["autoUse"]["gems"]["enabled"],
            "giveaway": self.config_dict["giveawayJoiner"]["enabled"],
            "hunt": self.config_dict["commands"]["hunt"]["enabled"],
            "level": self.config_dict["commands"]["lvlGrind"]["enabled"],
            "lottery": self.config_dict["commands"]["lottery"]["enabled"],
            "others": True,
            "owo": self.config_dict["commands"]["owo"]["enabled"],
            "pray": self.config_dict["commands"]["pray"]["enabled"],
            "sell": self.config_dict["commands"]["sell"]["enabled"],
            "shop": self.config_dict["commands"]["shop"]["enabled"],
            "slots": self.config_dict["gamble"]["slots"]["enabled"]
        }
        
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
                self.log(f"stuck {cmd_data}", "#d787ff")
            await self.queue.put(cmd_data)
        except Exception as e:
            print(e)
            print("^ at put_queue")
    
    async def remove_queue(self, cmd_data=None, id=None):
        if not cmd_data and not id:
            print("invalid id/cmd_data")
            return
        try:
            for index, (command, _) in enumerate(self.checks):
                async with self.lock:
                    if cmd_data:
                        if command == cmd_data:
                            self.checks[index][0]["removed"] = True
                            self.log(f"removing {cmd_data}", "#d787ff")
                    else:
                        if command.get("id", None) == id:
                            self.checks[index][0]["removed"] = True
                            self.log(f"removing {id}", "#d787ff")
        except Exception as e:
            print(e)



    def log(self, text, color, bold=False, debug=config_dict["debug"]["enabled"], save_log=config_dict["debug"]["logInTextFile"], web_log=config_dict["website"]["enabled"]):
        global website_logs
        style = f"{color} "
        if debug:
            frame_info = traceback.extract_stack()[-2]
            filename = os.path.basename(frame_info.filename)
            lineno = frame_info.lineno
            current_time = datetime.now().strftime("%H:%M:%S")
            content_to_print = f"[{current_time}] {text} | [{filename}:{lineno}]"
            console.print(content_to_print, style=style, markup=False)
            with lock:
                if save_log:
                    with open("logs.txt", "a") as log:
                        log.write(f"{content_to_print}\n")
        else:
            console.print(text.center(console_width - 2), style=style)
        if web_log:
            with lock:
                website_logs.append(f"<p style='color: {color};'>{self.user}| {text}</p>")
                if len(website_logs) > 10:
                    website_logs.pop(0)



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
    
    def time_in_seconds(self):
        """
        timestamp is basically seconds passed after 1970 jan 1st
        """
        time_now = datetime.now(timezone.utc).astimezone(pytz.timezone('US/Pacific'))
        return time_now.timestamp()

    async def on_ready(self):
        #self.on_ready_dn = False
        self.owo_bot_id = 408785106942164992
        if self.session is None:
            self.session = aiohttp.ClientSession()
        await asyncio.sleep(self.random_float(config_dict["account"]["startupDelay"]))
        printBox(f'-Loaded {self.user.name}[*].'.center(console_width - 2 ),'bold royal_blue1 ' )
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
        self.config_update_checker.start()
        await self.update_config()
        

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
    printBox(f'-Made by EchoQuill'.center(console_width - 2 ),'bold grey30' )
    #printBox(f'-Current Version:- {version}'.center(console_width - 2 ),'bold spring_green4' )
    tokens_and_channels = [line.strip().split() for line in open("tokens.txt", "r")]
    token_len = len(tokens_and_channels)
    printBox(f'-Recieved {token_len} tokens.'.center(console_width - 2 ),'bold magenta' )
    if config_dict["website"]["enabled"]:
        printBox(f'Website Dashboard: http://localhost:{config_dict["website"]["port"]}'.center(console_width - 2 ), 'dark_magenta')
    try:
        news_json = requests.get(f"{owo_dusk_api}/news.json").json()
        if news_json["available"]:
            printBox(f'{news_json["content"]}'.center(console_width - 2 ),'bold aquamarine1', title=news_json["title"] )
    except Exception as e:
        print(e)
    console.print("Star the repo in our github page if you want us to continue maintaining this proj :>.", style = "thistle1")
    console.rule(style="navy_blue")
    run_bots(tokens_and_channels)
    
