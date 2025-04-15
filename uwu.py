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
from discord.ext import commands, tasks
from rich.console import Console
from threading import Thread
from rich.panel import Panel
from rich.align import Align
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from copy import deepcopy
from utils.misspell import misspell_word
import json
import discord
import asyncio
import logging
import random
import traceback
import subprocess
import threading
import itertools
import aiohttp
import json
import pytz
import sys
import os
import time
import requests
import signal
import socket

"""Cntrl+c detect"""
def handle_sigint(signal_number, frame):
    print("\nCtrl+C detected. stopping code!")
    os._exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def compare_versions(current_version, latest_version):
    current_version = current_version.lstrip("v")
    latest_version = latest_version.lstrip("v")

    current = list(map(int, current_version.split(".")))
    latest = list(map(int, latest_version.split(".")))

    for c, l in zip(current, latest):
        if l > c:
            return True
        elif l < c:
            return False

    if len(latest) > len(current):
        return any(x > 0 for x in latest[len(current):])
    
    return False


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

with open("misc.json", "r") as config_file:
    misc_dict = json.load(config_file)


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
version = "2.1.0"
debug_print = True


"""FLASK APP"""

app = Flask(__name__)
website_logs = []
config_updated = None

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
    password = request.headers.get('password')
    if not password or password != config_dict["website"]["password"]:
        return "Invalid Password", 401
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
        config_updated = time.time()


        return jsonify({"status": "success", "message": "Data received and saved successfully"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "An error occurred while saving data"}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    password = request.headers.get('password')
    if not password or password != config_dict["website"]["password"]:
        return "Invalid Password", 401
    with open("config.json", "r") as file:
        config_data = json.load(file)
    return jsonify(config_data)


@app.route('/api/console', methods=['GET'])
def get_console_logs():
    password = request.headers.get('password')
    if not password or password != config_dict["website"]["password"]:
        return "Invalid Password", 401
    try:
        log_string = '\n'.join(website_logs)
        return log_string
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return jsonify({"status": "error", "message": "An error occurred while fetching logs"}), 500


def web_start():
    flaskLog = logging.getLogger("werkzeug")
    flaskLog.disabled = True
    cli = sys.modules["flask.cli"]
    cli.show_server_banner = lambda *x: None
    try:
        app.run(
            debug=False,
            use_reloader=False,
            port=config_dict["website"]["port"],
            host="0.0.0.0" if config_dict["website"]["enableHost"] else "127.0.0.1",
        )
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
    if not misc_dict["console"]["compactMode"]:
        console.print(test_panel)
    else:
        console.print(text, style=color)

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

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

if not on_mobile and not misc_dict["hostMode"]:
    try:
        if config_dict["batteryCheck"]["enabled"]:
            import psutil
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

def show_popup_thread():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    while True:
        msg, username, channelname, captchatype = popup_queue.get()
        print(msg, username, channelname, captchatype)
        # Create a new popup window
        popup = tk.Toplevel(root)
        popup.configure(bg="#000000")
        try:
            icon_path = "static/imgs/logo.png"  # Path to your icon image file
            icon = tk.PhotoImage(file=icon_path)
            popup.iconphoto(True, icon)
        except Exception as e:
            print(f"Failed to load icon: {e}")
        # Determine screen dimensions
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        # Calculate popup window position and size
        popup_width = min(500, int(screen_width * 0.8))  # Limit maximum width to 500px or 80% of screen width
        popup_height = min(300, int(screen_height * 0.8))  # Limit maximum height to 300px or 80% of screen height
        x_position = (screen_width - popup_width) // 2
        y_position = (screen_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")
        popup.title("OwO-dusk - Notifs")
        label_text = msg.format(username=username, channelname=channelname, captchatype=captchatype)
        label = tk.Label(
            popup, 
            text=label_text, 
            wraplength=popup_width - 40, 
            justify="left", 
            padx=20, 
            pady=20, 
            bg="#000000", 
            fg="#be7dff"
        )
        label.pack(fill="both", expand=True)
        button = tk.Button(popup, text="OK", command=popup.destroy)
        button.pack(pady=10)
        try:
            popup.grab_set()  # Restrict input focus to the popup
        except tk.TclError as e:
            print(f"Grab failed: {e}")
        finally:
            popup.focus_set()  # Ensure the popup has focus
            popup.lift()  # Bring the popup to the top

        popup.wait_window()


if config_dict["captcha"]["toastOrPopup"] and not on_mobile and not misc_dict["hostMode"]:
    try:
        import tkinter as tk
        from tkinter import PhotoImage
        from queue import Queue
    except Exception as e:
        print(f"ImportError: {e}")
        
    popup_queue = Queue()
    popup_thread = threading.Thread(target=show_popup_thread)
    popup_thread.daemon = True  # Ensure the thread exits when the main program does
    popup_thread.start()

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
        self.state_event = asyncio.Event()
        self.captcha = False
        self.balance = 0
        self.queue = asyncio.PriorityQueue()
        self.config_dict = None
        self.commands_dict = {}
        self.lock = asyncio.Lock()
        self.cash_check = False
        self.gain_or_lose = 0
        self.checks = []
        self.dm, self.cm = None,None
        self.sleep = False
        self.username = None
        self.last_cmd_ran = None
        self.reaction_bot_id = 519287796549156864
        self.cmd_counter = itertools.count()
        """self.user_data = {
            "balance": 0,
            "essence": 0,
            "server_id": 0,
            "animals_caught": 0,
            "hunts": 0,
            "battles": 0,
            "hb": 0,
            "giveaway": 0,
            "captchas": 0
        }"""

        with open("alias.json", "r") as config_file:
            self.alias = json.load(config_file)

        with open("misc.json", "r") as config_file:
            self.misc = json.load(config_file)

        self.cmds_state = {
            "global": {
                "last_ran": 0
            }
        }
        for key in self.misc["command_priority"]:
            self.cmds_state[key] = {
                "in_queue": False,
                "in_monitor": False,
                "last_ran": 0
            }

        if self.misc["debug"]["hideUser"]:
            """TASK: Ability to edit x/y"""
            x = ["cat", "dog", "wut", "idk", "noob", "pro", "gamer", "real", "fake", "notsoreal", "asreal", "hii"]
            y = ["123", "345", "234234", "catts", "fish", "dusk", "dawn", "op", "?", "new", "old", "epic", "duh"]
            self.username = f"{random.choice(x)}{random.choice(y)}"

    async def set_stat(self, value):
        if value:
            self.state = True
            self.state_event.set()
        else:
            while not self.state:
                await self.state_event.wait()
            self.state = False
            self.state_event.clear()

    @tasks.loop(seconds=30)
    async def presence(self):
        if self.status != discord.Status.invisible:
            try:
                await self.change_presence(
                status=discord.Status.invisible, activity=self.activity
            )
                self.presence.stop()
            except:
                pass
        else:
            self.presence.stop()

    @tasks.loop(seconds=5)
    async def config_update_checker(self):
        global config_updated
        if config_updated is not None and (time.time() - config_updated < 6):
            await self.update_config()
            # config_updated = False

    @tasks.loop(seconds=1)
    async def random_sleep(self):
        await asyncio.sleep(self.random_float(self.config_dict["sleep"]["checkTime"]))
        if random.randint(1, 100) > (100 - self.config_dict["sleep"]["frequencyPercentage"]):
            await self.set_stat(False)
            sleep_time = self.random_float(self.config_dict["sleep"]["sleeptime"])
            await self.log(f"sleeping for {sleep_time}", "#87af87")
            await asyncio.sleep(sleep_time)
            await self.set_stat(True)
            await self.log("sleeping finished!", "#87af87")

    @tasks.loop(seconds=7)
    async def safety_check_loop(self):
        safety_check = requests.get(f"{owo_dusk_api}/safety_check.json").json()
        latest_version = requests.get(f"{owo_dusk_api}/safety_check.json").json()

        if compare_versions(version, safety_check["version"]):
            self.captcha = True
            await self.log(f"There seems to be something wrong...\nStopping code for reason: {safety_check['reason']}\n(This was triggered by {safety_check['author']})", "#5c0018")
            if compare_versions(latest_version["version"], safety_check["version"]):
                await self.log(f"please update to: v{latest_version['version']}", "#33245e")

    async def start_cogs(self):
        files = os.listdir(resource_path("./cogs"))  # Get the list of files
        random.shuffle(files)
        self.refresh_commands_dict()
        for filename in files:
            if filename.endswith(".py"):

                extension = f"cogs.{filename[:-3]}"
                if extension in self.extensions:
                    """skip if already loaded"""
                    self.refresh_commands_dict()
                    if not self.commands_dict[str(filename[:-3])]:
                        await self.unload_cog(extension)
                    continue
                try:
                    await asyncio.sleep(self.random_float(self.config_dict["account"]["commandsStartDelay"]))
                    await self.load_extension(extension)
                    
                except Exception as e:
                    await self.log(f"Failed to load extension {extension}: {e}")


    async def update_config(self):
        async with self.lock:
            with open("config.json", "r") as config_file:
                self.config_dict = json.load(config_file)
            await self.start_cogs()

    async def unload_cog(self, cog_name):
        try:
            if cog_name in self.extensions:
                await self.unload_extension(cog_name)
        except Exception as e:
            await self.log(f"Error - Failed to unload cog {cog_name}: {e}")

    def refresh_commands_dict(self):
        commands_dict = self.config_dict["commands"]
        reaction_bot_dict = self.config_dict["defaultCooldowns"]["reactionBot"]
        self.commands_dict = {
            "battle": commands_dict["battle"]["enabled"] and not reaction_bot_dict["hunt_and_battle"],
            "captcha": True,
            "chat": True,
            "coinflip": self.config_dict["gamble"]["coinflip"]["enabled"],
            "commands": True,
            "cookie": commands_dict["cookie"]["enabled"],
            "daily": self.config_dict["autoDaily"],
            "gems": self.config_dict["autoUse"]["gems"]["enabled"],
            "giveaway": self.config_dict["giveawayJoiner"]["enabled"],
            "hunt": commands_dict["hunt"]["enabled"] and not reaction_bot_dict["hunt_and_battle"],
            "huntbot": commands_dict["autoHuntBot"]["enabled"],
            "level": commands_dict["lvlGrind"]["enabled"],
            "lottery": commands_dict["lottery"]["enabled"],
            "others": True,
            "owo": commands_dict["owo"]["enabled"] and not reaction_bot_dict["owo"],
            "pray": commands_dict["pray"]["enabled"] and not reaction_bot_dict["pray_and_curse"],
            "reactionbot": reaction_bot_dict["hunt_and_battle"] or reaction_bot_dict["owo"] or reaction_bot_dict["pray_and_curse"],
            "sell": commands_dict["sell"]["enabled"],
            "shop": commands_dict["shop"]["enabled"],
            "slots": self.config_dict["gamble"]["slots"]["enabled"]
        }

    """To make the code cleaner when accessing cooldowns from config."""
    def random_float(self, cooldown_list):
        return random.uniform(cooldown_list[0],cooldown_list[1])

    async def sleep_till(self, cooldown, cd_list=True, noise=3):
        if cd_list:
            await asyncio.sleep(
                random.uniform(cooldown[0],cooldown[1])
            )
        else:
            await asyncio.sleep(
                random.uniform(
                    cooldown,
                    cooldown + noise
                )
            )

    async def upd_cmd_state(self, id, reactionBot=False):
        async with self.lock:
            self.cmds_state["global"]["last_ran"] = time.time()
            self.cmds_state[id]["last_ran"] = time.time()
            if not reactionBot:
                self.cmds_state[id]["in_queue"] = False

    def construct_command(self, data):
        prefix = self.config_dict['setprefix'] if data.get("prefix") else ""
        return f"{prefix}{data['cmd_name']} {data.get('cmd_arguments', '')}".strip()

    async def put_queue(self, cmd_data, priority=False):
        cnf = self.misc["command_priority"]
        try:
            while not self.state or self.sleep or self.captcha:
                if priority:
                    break
                await asyncio.sleep(random.uniform(1.4, 2.9))
            
            if self.cmds_state[cmd_data["id"]]["in_queue"]:
                # Ensure command already in queue is not readded to prevent spam
                await self.log(f"Error - command with id: {cmd_data['id']} already in queue, being attempted to be added back.", "#c25560")
                return
            
            # Get priority
            priority_int = cnf[cmd_data["id"]].get("priority")
            if not priority_int:
                await self.log(f"Error - command with id: {cmd_data['id']} do not have a priority set in misc.json", "#c25560")
                return
            
            async with self.lock:
                await self.queue.put((
                    cnf[cmd_data["id"]]["priority"],  # Priority to sort commands with
                    next(self.cmd_counter),               # A counter to serve as a tie-breaker
                    deepcopy(cmd_data)                # actual data
                ))
                self.cmds_state[cmd_data["id"]]["in_queue"] = True
        except Exception as e:
            await self.log(f"Error - {e}, during put_queue", "#c25560")

    async def remove_queue(self, cmd_data=None, id=None):
        if not cmd_data and not id:
            await self.log(f"Error: No id or command data provided for removing item from queue.", "#c25560")
            return
        try:
            async with self.lock:
                for index, command in enumerate(self.checks):
                    if cmd_data:
                        if command == cmd_data:
                            self.checks.pop(index)
                    else:
                        if command.get("id", None) == id:
                            self.checks.pop(index)
        except Exception as e:
            await self.log(f"Error: {e}, during remove_queue", "#c25560")

    async def search_checks(self, id):
        async with self.lock:
            for command, _ in self.checks:
                if command.get("id", None) == id:
                    return True
            return False

    async def shuffle_queue(self):
        async with self.lock:
            items = []
            while not self.queue.empty():
                items.append(await self.queue.get())

            random.shuffle(items)

            for item in items:
                await self.queue.put(item)

    def add_popup_queue(self, channel_name, captcha_type=None):
        with lock:
            popup_queue.put(
                (
                    (
                        config_dict["captcha"]["toastOrPopup"]["captchaContent"]
                        if captcha_type != "Ban"
                        else config_dict["captcha"]["toastOrPopup"]["bannedContent"]
                    ),
                    self.user.name,
                    channel_name,
                    captcha_type,
                )
            )

    async def log(self, text, color, bold=False, web_log=config_dict["website"]["enabled"], webhook_useless_log=config_dict["webhook"]["webhookUselessLog"]):
        global website_logs
        current_time = datetime.now().strftime("%H:%M:%S")
        if self.misc["debug"]["enabled"]:
            frame_info = traceback.extract_stack()[-2]
            filename = os.path.basename(frame_info.filename)
            lineno = frame_info.lineno

            content_to_print = f"[{current_time}] {self.username} - {text} | [{filename}:{lineno}]"
            console.print(content_to_print, style=color, markup=False)
            with lock:
                if self.misc["debug"]["logInTextFile"]:
                    with open("logs.txt", "a") as log:
                        log.write(f"{content_to_print}\n")
        else:
            console.print(f"{self.username}| {text}".center(console_width - 2), style=color)
        if web_log:
            with lock:
                website_logs.append(f"<p style='color: {color};'>[{current_time}] {self.username}| {text}</p>")
                if len(website_logs) > 10:
                    website_logs.pop(0)
        if webhook_useless_log:
            await self.webhookSender(footer=f"[{current_time}] {self.username} - {text}", colors=color)

    async def webhookSender(self, msg=None, desc=None, plain_text=None, colors=None, img_url=None, author_img_url=None, footer=None, webhook_url=None):
        try:
            if colors:
                if isinstance(colors, str) and colors.startswith("#"):
                    """Convert to hexadecimal value"""
                    color = discord.Color(int(colors.lstrip("#"), 16))
                else:
                    color = discord.Color(colors)
            else:
                color = discord.Color(0x412280)

            emb = discord.Embed(
                title=msg,
                description=desc,
                color=color
            )
            if footer:
                emb.set_footer(text=footer)
            if img_url:
                emb.set_thumbnail(url=img_url)
            if author_img_url:
                emb.set_author(name=self.username, icon_url=author_img_url)
            webhook = discord.Webhook.from_url(self.config_dict["webhook"]["webhookUrl"] if not webhook_url else webhook_url, session=self.session)
            if plain_text:
                await webhook.send(content=plain_text, embed=emb, username='OwO-Dusk')
            else:
                await webhook.send(embed=emb, username='OwO-Dusk')
        except discord.Forbidden as e:
            await self.log(f"Error - {e}, during webhookSender. Seems like permission missing.", "#c25560")
        except Exception as e:
            await self.log(f"Error - {e}, during webhookSender.")

    def calculate_correction_time(self, command):
        command = command.replace(" ", "")  # Remove spaces for accurate timing
        base_delay = self.random_float(self.config_dict["misspell"]["baseDelay"]) 
        rectification_time = sum(self.random_float(self.config_dict["misspell"]["errorRectificationTimePerLetter"]) for _ in command)  
        total_time = base_delay + rectification_time
        return total_time

    # send commands
    async def send(self, message, bypass=False, channel=None, silent=config_dict["silentTextMessages"], typingIndicator=config_dict["typingIndicator"]):
        """
            TASK: Refactor
        """

        if not channel:
            channel = self.cm
        disable_log = self.misc["console"]["disableCommandSendLog"]
        msg = message
        misspelled = False
        if self.config_dict["misspell"]["enabled"]:
            if random.uniform(1,100) < self.config_dict["misspell"]["frequencyPercentage"]:
                msg = misspell_word(message)
                misspelled = True
                # left off here!

        """
        TASK: remove repition here
        """
        if not self.captcha or bypass:
            await self.wait_until_ready()
            if typingIndicator:
                async with channel.typing():
                    await channel.send(msg, silent=silent)
            else:
                await channel.send(msg, silent=silent)
            if not disable_log:
                await self.log(f"Ran: {msg}", "#5432a8")
            if misspelled:
                await self.set_stat(False)
                time = self.calculate_correction_time(message)
                await self.log(f"correcting: {msg} -> {message} in {time}s", "#5432a8")
                await asyncio.sleep(time)
                if typingIndicator:
                    async with channel.typing():
                        await channel.send(message, silent=silent)
                else:
                    await channel.send(message, silent=silent)
                await self.set_stat(True)

    async def slashCommandSender(self, msg, **kwargs):
        try:
            for command in self.slash_commands:
                if command.name == msg:
                    await self.wait_until_ready()
                    await command(**kwargs)
                    await self.log(f"Ran: /{msg}", "#5432a8")
        except Exception as e:
            await self.log(f"Error: {e}, during slashCommandSender", "#c25560")

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

    async def check_for_cash(self):
        await asyncio.sleep(random.uniform(4.5, 6.4))
        await self.put_queue(
            {
                "cmd_name": self.alias["cash"]["normal"],
                "prefix": True,
                "checks": True,
                "id": "cash",
                "removed": False
            }
        )

    """async def on_ready(self):
        if not self.dm:
            # Temporary fix for https://github.com/dolfies/discord.py-self/issues/744
            try:
                self.dm = await (self.get_user(self.owo_bot_id)).create_dm()

                if self.dm is None:
                    self.dm = await self.fetch_user(self.owo_bot_id).create_dm()

            except discord.Forbidden as e:
                await self.log(f"Error: {e}, Attempting to get user with the help of {self.cm}", "#c25560")
                await self.cm.send(f"{config_dict['setprefix']}ping")
                async for message in self.cm.history(limit=10):
                    if message.author.id == self.owo_bot_id:
                        self.dm = await message.author.create_dm()
                        break
                await asyncio.sleep(random.uniform(0.5, 0.9))
            except Exception as e:
                await self.log(f"Error: {e}, during", "#c25560")"""

    async def setup_hook(self):
        if not self.username:
            self.username = self.user.name
        self.owo_bot_id = 408785106942164992
        self.dm = None
        self.safety_check_loop.start()
        if self.session is None:
            self.session = aiohttp.ClientSession()

        printBox(f'-Loaded {self.username}[*].'.center(console_width - 2), 'bold royal_blue1 ')
        listUserIds.append(self.user.id)

        # Fetch the channel
        self.cm = self.get_channel(self.channel_id)
        if not self.cm:
            try:
                self.cm = await self.fetch_channel(self.channel_id)
            except discord.NotFound:
                await self.log(f"Error - Channel with ID {self.channel_id} does not exist.", "#c25560")
                return
            except discord.Forbidden:
                await self.log(f"Bot lacks permissions to access channel {self.channel_id}.", "#c25560")
                return
            except discord.HTTPException as e:
                await self.log(f"Failed to fetch channel {self.channel_id}: {e}", "#c25560")
                return

        self.dm = await (await self.fetch_user(self.owo_bot_id)).create_dm()

        # Fetch slash commands in self.cm
        self.slash_commands = []
        for command in await self.cm.application_commands():
            if command.application.id == self.owo_bot_id:
                self.slash_commands.append(command)

        # Add account to stats.json
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

        # Start various tasks and updates
        self.config_update_checker.start()
        await asyncio.sleep(self.random_float(config_dict["account"]["startupDelay"]))
        print("upd config")
        await self.update_config()
        print("updated cnfg")

        if self.config_dict["offlineStatus"]:
            self.presence.start()

        if self.config_dict["sleep"]["enabled"]:
            self.random_sleep.start()

        if self.config_dict["cashCheck"]:
            asyncio.create_task(self.check_for_cash())
        print("---- ed -----")

def get_local_ip():
    if not config_dict["website"]["enableHost"]:
        return 'localhost'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            """10.255.255.255 is fake"""
            s.connect(('10.255.255.255', 1))
            return s.getsockname()[0]
    except Exception:
        return 'localhost'

# ----------STARTING BOT----------#
def fetch_json(url, description="data"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        printBox(f"Failed to fetch {description}: {e}", "bold red")
        return {}

def run_bots(tokens_and_channels):
    threads = []
    for token, channel_id in tokens_and_channels:
        thread = Thread(target=run_bot, args=(token, channel_id))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def run_bot(token, channel_id):
    try:
        logging.getLogger("discord.client").setLevel(logging.ERROR)
        client = MyClient(token, channel_id)
        client.run(token, log_level=logging.ERROR)
    except Exception as e:
        printBox(f"Error starting bot with token {token}...: {e}", "bold red")

if __name__ == "__main__":
    if not misc_dict["console"]["compactMode"]:
        console.print(owoPanel)
        console.rule(f"[bold blue1]version - {version} beta", style="navy_blue")
    version_json = fetch_json(f"{owo_dusk_api}/version.json", "version info")

    if compare_versions(version, version_json["version"]):
        printBox(f"""Update Detected - {version_json["version"]}
    Changelog:-
        {version_json["changelog"]}""",'bold gold3')
        if version_json["important_update"]:
            printBox('It is reccomended to update....','bold light_yellow3' )

    tokens_and_channels = [line.strip().split() for line in open("tokens.txt", "r")]
    token_len = len(tokens_and_channels)

    printBox(f'-Recieved {token_len} tokens.'.center(console_width - 2 ),'bold magenta' )

    if config_dict["website"]["enabled"]:
        ip = get_local_ip()
        printBox(f'Website Dashboard: http://{ip}:{config_dict["website"]["port"]}'.center(console_width - 2 ), 'dark_magenta')

    try:
        if misc_dict["news"]:
            news_json = fetch_json(f"{owo_dusk_api}/news.json", "news")
            if news_json.get("available"):
                printBox(
                    f'{news_json.get("content", "no content found..? this is an error! should be safe to ignore")}'.center(console_width - 2),
                    f"bold {news_json.get('color', 'white')}",
                    title=news_json.get("title", "???")
                )
    except Exception as e:
        print(e)

    if not misc_dict["console"]["hideStarRepoMessage"]:
        console.print("Star the repo in our github page if you want us to continue maintaining this proj :>.", style = "thistle1")
    console.rule(style="navy_blue")
    run_bots(tokens_and_channels)
