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

# Standard Library
import asyncio
import itertools
import json
import logging
import os
import random
import signal
import socket
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
from importlib.metadata import version as import_ver
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from threading import Thread
# Third-Party Libraries
import aiosqlite
import aiohttp
import discord
import pytz
import requests
from discord.ext import commands, tasks
from flask import Flask, jsonify, render_template, request
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
# Local
from utils.misspell import misspell_word


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

with open("config/global_settings.json", "r") as config_file:
    global_settings_dict = json.load(config_file)

with open("config/misc.json", "r") as config_file:
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
version = "2.2.0"
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

def get_from_db(command):
    with sqlite3.connect("utils/data/db.sqlite") as conn:
        conn.row_factory = sqlite3.Row 
        cur = conn.cursor()

        cur.execute("PRAGMA journal_mode;")
        mode = cur.fetchone()[0]
        if mode.lower() != 'wal':
            cur.execute("PRAGMA journal_mode=WAL;")

        cur.execute(command)

        item = cur.fetchall()
        return item


@app.route("/")
def home():
    return render_template("index.html", version=version)


@app.route('/api/console', methods=['GET'])
def get_console_logs():
    password = request.headers.get('password')
    if not password or password != global_settings_dict["website"]["password"]:
        return "Invalid Password", 401
    try:
        log_string = '\n'.join(website_logs)
        return log_string
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return jsonify({"status": "error", "message": "An error occurred while fetching logs"}), 500

@app.route('/api/fetch_gamble_data', methods=['GET'])
def fetch_gamble_data():
    password = request.headers.get('password')
    if not password or password != global_settings_dict["website"]["password"]:
        return "Invalid Password", 401
    try:
        # Fetch table data
        rows = get_from_db("SELECT hour, wins, losses FROM gamble_winrate ORDER BY hour")

        # Extract columns as lists
        win_data = [row["wins"] for row in rows]
        lose_data = [row["losses"] for row in rows]

        # Return Data
        return jsonify({
            "status": "success",
            "win_data": win_data,
            "lose_data": lose_data
        })
        
    except Exception as e:
        print(f"Error fetching gamble data: {e}")
        return jsonify({"status": "error", "message": "An error occurred while fetching gamble data"}), 500

@app.route('/api/fetch_cowoncy_data', methods=['GET'])
def fetch_cowoncy_data():
    password = request.headers.get('password')
    if not password or password != global_settings_dict["website"]["password"]:
        return "Invalid Password", 401

    try:
        rows = get_from_db("SELECT user_id, hour, earnings FROM cowoncy_earnings ORDER BY hour")
        user_data = {}
        for row in rows:
            user_id = row["user_id"]
            hour = row["hour"]
            earnings = row["earnings"]

            if user_id not in user_data:
                # Create dummy data
                user_data[user_id] = {i: 0 for i in range(24)}
            # populate
            user_data[user_id][hour] = earnings

        # Base data
        base_data = {
            "labels": [f"Hour {i}" for i in range(24)],
            "datasets": []
        }

        for user_id, hourly_data in user_data.items():
            color_hue = random.randint(0, 360)
            dataset = {
                "label": user_id,
                "data": [hourly_data[i] for i in range(24)],
                "borderColor": f"hsl({color_hue}, 100%, 50%)",
                "backgroundColor": f"hsl({color_hue}, 100%, 70%)",
                "fill": True,
                "tension": 0.4,
                "pointRadius": 0,
            }
            base_data["datasets"].append(dataset)

        
        rows = get_from_db("SELECT cowoncy, captchas FROM user_stats")
        total_cowoncy = sum(row["cowoncy"] for row in rows)
        # I understand this area is for cowoncy, but accessing thro here since lazy lol.
        total_captchas = sum(row["captchas"] for row in rows)


        return jsonify({
            "status": "success",
            "data": base_data,
            "total_cash": total_cowoncy,
            "total_captchas": total_captchas
        }), 200

    except Exception as e:
        print(f"Error fetching cowoncy data: {e}")
        return jsonify({
            "status": "error",
            "message": "An error occurred while fetching cowoncy data"
        }), 500

@app.route('/api/fetch_cmd_data', methods=['GET'])
def fetch_cmd_data():
    password = request.headers.get('password')
    if not password or password != global_settings_dict["website"]["password"]:
        return "Invalid Password", 401
    try:
        rows = get_from_db("SELECT * FROM commands")

        filtered_rows = [row for row in rows if row["count"] != 0]

        command_names = [row["name"] for row in filtered_rows]
        count = [row["count"] for row in filtered_rows]

        for idx, item in enumerate(count):
            if item == 0:
                command_names.pop(idx)
                count.pop(idx)


        # Return Data
        return jsonify({
            "status": "success",
            "command_names": command_names,
            "count": count
        })
        
    except Exception as e:
        print(f"Error fetching command data: {e}")
        return jsonify({"status": "error", "message": "An error occurred while fetching command data"}), 500

@app.route('/api/fetch_weekly_runtime', methods=['GET'])
def fetch_weekly_runtime():
    password = request.headers.get('password')
    if not password or password != global_settings_dict["website"]["password"]:
        return "Invalid Password", 401
    try:
        # Fetch json data
        with open("utils/data/weekly_runtime.json", "r") as config_file:
            data_dict = json.load(config_file)
        
        runtime_data = [(val[1] - val[0]) / 60 for val in data_dict.values() if isinstance(val, list)]

        cur_hour = get_weekday()

        # Return Data
        return jsonify({
            "status": "success",
            "runtime_data": runtime_data,
            "current_uptime": data_dict[cur_hour]
        })
        
    except Exception as e:
        print(f"Error fetching weekly runtime: {e}")
        return jsonify({"status": "error", "message": "An error occurred while fetching weekly runtime"}), 500


def web_start():
    flaskLog = logging.getLogger("werkzeug")
    flaskLog.disabled = True
    cli = sys.modules["flask.cli"]
    cli.show_server_banner = lambda *x: None
    app.run(
        debug=False,
        use_reloader=False,
        port=global_settings_dict["website"]["port"],
        host="0.0.0.0" if global_settings_dict["website"]["enableHost"] else "127.0.0.1",
    )


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
        if global_settings_dict["batteryCheck"]["enabled"]:
            import psutil
    except Exception as e:
        print(f"ImportError: {e}")


# For time related stuff
def get_weekday():
    # 0 = monday, 6 = sunday
    return str(datetime.today().weekday())

def get_hour():
    # only from 0 to 23 (24hr format)
    return datetime.now().hour

def get_date():
    return datetime.now().date().isoformat()  # e.g. "2025-05-31"


# For battery check
def batteryCheckFunc():
    cnf = global_settings_dict["batteryCheck"]
    try:
        if on_mobile:
            while True:
                time.sleep(cnf["refreshInterval"])
                try:
                    battery_status = os.popen("termux-battery-status").read()
                except Exception as e:
                    console.print(
                        f"system - Battery check failed!!".center(console_width - 2),
                        style="red ",
                    )
                battery_data = json.loads(battery_status)
                percentage = battery_data["percentage"]
                console.print(
                    f"system - Current battery •> {percentage}".center(console_width - 2),
                    style="blue ",
                )
                if percentage < int(cnf["minPercentage"]):
                    break
        else:
            while True:
                time.sleep(cnf["refreshInterval"])
                try:
                    battery = psutil.sensors_battery()
                    if battery is not None:
                        percentage = int(battery.percent)
                        console.print(
                            f"system - Current battery •> {percentage}".center(console_width - 2),
                            style="blue ",
                        )
                        if percentage < int(cnf["minPercentage"]):
                            break
                except Exception as e:
                    console.print(
                        f"-system - Battery check failed!!.".center(console_width - 2),
                        style="red ",
                    )
    except Exception as e:
        print("battery check", e)
    os._exit(0)

if global_settings_dict["batteryCheck"]["enabled"]:
    loop_thread = threading.Thread(target=batteryCheckFunc, daemon=True)
    loop_thread.start()

def popup_main_loop():
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


class MyClient(commands.Bot):

    def __init__(self, token, channel_id, global_settings_dict, *args, **kwargs):
        super().__init__(command_prefix="-", self_bot=True, *args, **kwargs)
        self.token = token
        self.channel_id = int(channel_id)
        self.list_channel = [self.channel_id]
        self.session = None
        self.state_event = asyncio.Event()
        self.queue = asyncio.PriorityQueue()
        self.settings_dict = None
        self.global_settings_dict = global_settings_dict
        self.commands_dict = {}
        self.lock = asyncio.Lock()
        self.cash_check = False
        self.gain_or_lose = 0
        self.checks = []
        self.dm, self.cm = None,None
        self.username = None
        self.nick_name = None
        self.last_cmd_ran = None
        self.reaction_bot_id = 519287796549156864
        self.owo_bot_id = 408785106942164992
        self.cmd_counter = itertools.count()

        # discord.py-self's module sets global random to fixed seed. reset that, locally.
        self.random = random.Random()

        # Task: Update code to have checks using status instead of individual variables
        self.user_status = {
            "no_gems": False,
            "no_cash": False,
            "balance": 0,
            "net_earnings": 0
        }

        self.command_handler_status = {
            "state": True,
            "captcha": False,
            "sleep": False,
            "hold_handler": False
        }

        with open("config/misc.json", "r") as config_file:
            self.misc = json.load(config_file)

        self.alias = self.misc["alias"]

        self.cmds_state = {
            "global": {
                "last_ran": 0
            }
        }
        for key in self.misc["command_info"]:
            self.cmds_state[key] = {
                "in_queue": False,
                "in_monitor": False,
                "last_ran": 0
            }

    async def set_stat(self, value, debug_note=None):
        if value:
            self.command_handler_status["state"] = True
            self.state_event.set()
        else:
            while not self.command_handler_status["state"]:
                await self.state_event.wait()
            self.command_handler_status["state"] = False
            self.state_event.clear()

    async def empty_checks_and_switch(self, channel):
        self.command_handler_status["hold_handler"] = True
        await self.sleep_till(self.global_settings_dict["channelSwitcher"]["delayBeforeSwitch"])
        self.cm = channel
        self.command_handler_status["hold_handler"] = False

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
        sleep_dict = self.settings_dict["sleep"]
        await asyncio.sleep(self.random_float(sleep_dict["checkTime"]))
        if self.random.randint(1, 100) > (100 - sleep_dict["frequencyPercentage"]):
            await self.set_stat(False, "sleep")
            sleep_time = self.random_float(sleep_dict["sleeptime"])
            await self.log(f"sleeping for {sleep_time}", "#87af87")
            await asyncio.sleep(sleep_time)
            await self.set_stat(True, "sleep stop")
            await self.log("sleeping finished!", "#87af87")

    @tasks.loop(seconds=7)
    async def safety_check_loop(self):
        safety_check = requests.get(f"{owo_dusk_api}/safety_check.json").json()
        latest_version = requests.get(f"{owo_dusk_api}/safety_check.json").json()

        if compare_versions(version, safety_check["version"]):
            self.command_handler_status["captcha"] = True
            await self.log(f"There seems to be something wrong...\nStopping code for reason: {safety_check['reason']}\n(This was triggered by {safety_check['author']})", "#5c0018")
            if compare_versions(latest_version["version"], safety_check["version"]):
                await self.log(f"please update to: v{latest_version['version']}", "#33245e")

    async def start_cogs(self):
        files = os.listdir(resource_path("./cogs"))  # Get the list of files
        self.random.shuffle(files)
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
                    await asyncio.sleep(self.random_float(self.global_settings_dict["account"]["commandsStartDelay"]))
                    if self.commands_dict.get(str(filename[:-3]), False):
                        await self.load_extension(extension)

                except Exception as e:
                    await self.log(f"Error - Failed to load extension {extension}: {e}", "#c25560")

        if "cogs.captcha" not in self.extensions:
            await self.log(f"Error - Failed to load captcha extension,\nStopping code!!", "#c25560")
            os._exit(0)

    async def update_config(self):
        async with self.lock:
            custom_path = f"config/{self.user.id}.settings.json"
            default_config_path = "config/settings.json"

            config_path = custom_path if os.path.exists(custom_path) else default_config_path

            with open(config_path, "r") as config_file:
                self.settings_dict = json.load(config_file)

            await self.start_cogs()

    async def update_database(self, sql, params=None):
        async with aiosqlite.connect("utils/data/db.sqlite", timeout=5) as db:
            await db.execute("PRAGMA journal_mode=WAL;")
            await db.execute("PRAGMA synchronous=NORMAL;")
            await db.execute("BEGIN;")
            await db.execute(sql, params)
            await db.commit()

    async def get_from_db(self, sql, params=None):
        async with aiosqlite.connect("utils/data/db.sqlite", timeout=5) as db:
            # allows dictionary-like access
            db.row_factory = aiosqlite.Row
            async with db.execute(sql, params or ()) as cursor:
                result = await cursor.fetchall()
                return result

    async def update_cash_db(self):
        """Update values in database"""
        hr = get_hour()

        await self.update_database(
            """UPDATE cowoncy_earnings
            SET earnings = ?
            WHERE user_id = ? AND hour = ?;""",
            (self.user_status["net_earnings"], self.user.id, hr)
        )

        await self.update_database(
            "UPDATE user_stats SET cowoncy = ? WHERE user_id = ?",
            (self.user_status["balance"], self.user.id)
        )

    async def update_captcha_db(self):
        await self.update_database(
            "UPDATE user_stats SET captchas = captchas + 1 WHERE user_id = ?",
            (self.user.id,)
        )

    async def populate_stats_db(self):
        await self.update_database(
            "INSERT OR IGNORE INTO user_stats (user_id, daily, lottery, cookie, giveaways, captchas, cowoncy) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (self.user.id, 0, 0, 0, 0, 0, 0)
        )

    async def populate_cowoncy_earnings(self, update=False):
        today_str = get_date()

        for i in range(24):
            if not update:
                await self.update_database(
                    "INSERT OR IGNORE INTO cowoncy_earnings (user_id, hour, earnings) VALUES (?, ?, ?)",
                    (self.user.id, i, 0)
                )

        rows = await self.get_from_db(
            "SELECT value FROM meta_data WHERE key = ?", 
            ("cowoncy_earnings_last_checked",)
        )

        last_reset_str = rows[0]['value'] if rows else "0"

        if last_reset_str == today_str:
            # Handle gap between cowoncy chart
            cur_hr = get_hour()
            last_cash = 0
            for hr in range(cur_hr+1):
                hr_row = await self.get_from_db(
                    "SELECT earnings FROM cowoncy_earnings WHERE user_id = ? AND hour = ?", 
                    (self.user.id, hr)
                )
                # Note: negative values are allowed.
                if hr_row and hr_row[0]["earnings"] != 0:
                    last_cash = hr_row[0]["earnings"]
                elif last_cash != 0:
                    await self.update_database(
                        "UPDATE cowoncy_earnings SET earnings = ? WHERE hour = ? AND user_id = ?",
                        (last_cash, hr, self.user.id)
                    )
            # Return once done as we don't want reset.
            return

        for i in range(24):
            await self.update_database(
                "UPDATE cowoncy_earnings SET earnings = 0 WHERE user_id = ? AND hour = ?",
                (self.user.id, i)
            )

        await self.update_database(
            "UPDATE meta_data SET value = ? WHERE key = ?",
            (today_str, "cowoncy_earnings_last_checked")
        )

    async def fetch_net_earnings(self):
        self.user_status["net_earnings"] = 0
        rows = await self.get_from_db(
            "SELECT earnings FROM cowoncy_earnings WHERE user_id = ? ORDER BY hour",
            (self.user.id,)
        )

        cowoncy_list = [row["earnings"] for row in rows]

        for item in reversed(cowoncy_list):
            if item != 0:
                self.user_status["net_earnings"] = item
                break

    async def reset_gamble_wins_or_losses(self):
        today_str = get_date()

        rows = await self.get_from_db(
            "SELECT value FROM meta_data WHERE key = ?", 
            ("gamble_winrate_last_checked",)
        )

        last_reset_str = rows[0]['value'] if rows else "0"

        if last_reset_str == today_str:
            return

        for hour in range(24):
            await self.update_database(
                "UPDATE gamble_winrate SET wins = 0, losses = 0, net = 0 WHERE hour = ?",
                (hour,)
            )

        await self.update_database(
            "UPDATE meta_data SET value = ? WHERE key = ?",
            (today_str, "gamble_winrate_last_checked")
        )

    async def update_cmd_db(self, cmd):
        await self.update_database(
            "UPDATE commands SET count = count + 1 WHERE name = ?",
            (cmd,)
        )

    async def update_gamble_db(self, item="wins"):
        hr = get_hour()

        if item not in {"wins", "losses"}:
            raise ValueError("Invalid column name.")

        await self.update_database(
            f"UPDATE gamble_winrate SET {item} = {item} + 1 WHERE hour = ?",
            (hr,)
        )

    async def unload_cog(self, cog_name):
        try:
            if cog_name in self.extensions:
                await self.unload_extension(cog_name)
        except Exception as e:
            await self.log(f"Error - Failed to unload cog {cog_name}: {e}", "#c25560")

    def refresh_commands_dict(self):
        commands_dict = self.settings_dict["commands"]
        reaction_bot_dict = self.settings_dict["defaultCooldowns"]["reactionBot"]
        self.commands_dict = {
            "battle": commands_dict["battle"]["enabled"] and not reaction_bot_dict["hunt_and_battle"],
            "captcha": True,
            "channelswitcher": self.global_settings_dict["channelSwitcher"]["enabled"],
            "chat": True,
            "coinflip": self.settings_dict["gamble"]["coinflip"]["enabled"],
            "commands": True,
            "cookie": commands_dict["cookie"]["enabled"],
            "daily": self.settings_dict["autoDaily"],
            "gems": self.settings_dict["autoUse"]["gems"]["enabled"],
            "giveaway": self.settings_dict["giveawayJoiner"]["enabled"],
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
            "slots": self.settings_dict["gamble"]["slots"]["enabled"]
        }

    """To make the code cleaner when accessing cooldowns from config."""
    def random_float(self, cooldown_list):
        return self.random.uniform(cooldown_list[0],cooldown_list[1])

    async def sleep_till(self, cooldown, cd_list=True, noise=3):
        if cd_list:
            await asyncio.sleep(
                self.random.uniform(cooldown[0],cooldown[1])
            )
        else:
            await asyncio.sleep(
                self.random.uniform(
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
            await self.update_cmd_db(id)

    def construct_command(self, data):
        prefix = self.settings_dict['setprefix'] if data.get("prefix") else ""
        return f"{prefix}{data['cmd_name']} {data.get('cmd_arguments', '')}".strip()

    async def put_queue(self, cmd_data, priority=False, quick=False):
        cnf = self.misc["command_info"]
        try:
            while (
                not self.command_handler_status["state"]
                or self.command_handler_status["hold_handler"]
                or self.command_handler_status["sleep"]
                or self.command_handler_status["captcha"]
            ):
                if priority and (
                    not self.command_handler_status["sleep"]
                    and not self.command_handler_status["hold_handler"]
                    and not self.command_handler_status["captcha"]
                ):
                    break
                await asyncio.sleep(self.random.uniform(1.4, 2.9))

            if self.cmds_state[cmd_data["id"]]["in_queue"]:
                # Ensure command already in queue is not readded to prevent spam
                await self.log(f"Error - command with id: {cmd_data['id']} already in queue, being attempted to be added back.", "#c25560")
                return

            # Get priority
            priority_int = cnf[cmd_data["id"]].get("priority") if not quick else 0
            if not priority_int and priority_int!=0:
                await self.log(f"Error - command with id: {cmd_data['id']} do not have a priority set in misc.json", "#c25560")
                return

            async with self.lock:
                await self.queue.put((
                    priority_int,  # Priority to sort commands with
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
            for command in self.checks:
                if command.get("id", None) == id:
                    return True
            return False

    async def shuffle_queue(self):
        async with self.lock:
            items = []
            while not self.queue.empty():
                items.append(await self.queue.get())

            self.random.shuffle(items)

            for item in items:
                await self.queue.put(item)

    def add_popup_queue(self, channel_name, captcha_type=None):
        with lock:
            popup_queue.put(
                (
                    (
                        global_settings_dict["captcha"]["toastOrPopup"]["captchaContent"]
                        if captcha_type != "Ban"
                        else global_settings_dict["captcha"]["toastOrPopup"]["bannedContent"]
                    ),
                    self.user.name,
                    channel_name,
                    captcha_type,
                )
            )

    async def log(self, text, color="#ffffff", bold=False, web_log=global_settings_dict["website"]["enabled"], webhook_useless_log=global_settings_dict["webhook"]["webhookUselessLog"]):
        global website_logs
        current_time = datetime.now().strftime("%H:%M:%S")
        if self.misc["debug"]["enabled"]:
            frame_info = traceback.extract_stack()[-2]
            filename = os.path.basename(frame_info.filename)
            lineno = frame_info.lineno

            content_to_print = f"[#676585]❲{current_time}❳[/#676585] {self.username} - {text} | [#676585]❲{filename}:{lineno}❳[/#676585]"
            console.print(
                content_to_print,
                style=color,
                markup=True
            )
            with lock:
                if self.misc["debug"]["logInTextFile"]:
                    with open("logs.txt", "a") as log:
                        log.write(f"{content_to_print}\n")
        else:
            console.print(f"{self.username}| {text}".center(console_width - 2), style=color)
        if web_log:
            with lock:
                website_logs.append(f"<div class='message'><span class='timestamp'>[{current_time}]</span><span class='text'>{self.username}| {text}</span></div>")
                if len(website_logs) > 300:
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
            webhook = discord.Webhook.from_url(self.global_settings_dict["webhook"]["webhookUrl"] if not webhook_url else webhook_url, session=self.session)
            if plain_text:
                await webhook.send(content=plain_text, embed=emb, username='OwO-Dusk')
            else:
                await webhook.send(embed=emb, username='OwO-Dusk')
        except discord.Forbidden as e:
            await self.log(f"Error - {e}, during webhookSender. Seems like permission missing.", "#c25560")
        except Exception as e:
            await self.log(f"Error - {e}, during webhookSender.", "#c25560")

    def calculate_correction_time(self, command):
        command = command.replace(" ", "")  # Remove spaces for accurate timing
        base_delay = self.random_float(self.settings_dict["misspell"]["baseDelay"]) 
        rectification_time = sum(self.random_float(self.settings_dict["misspell"]["errorRectificationTimePerLetter"]) for _ in command)  
        total_time = base_delay + rectification_time
        return total_time

    # send commands
    async def send(self, message, color=None, bypass=False, channel=None, silent=global_settings_dict["silentTextMessages"], typingIndicator=global_settings_dict["typingIndicator"]):
        """
            TASK: Refactor
        """

        if not channel:
            channel = self.cm
        disable_log = self.misc["console"]["disableCommandSendLog"]
        msg = message
        misspelled = False
        if self.settings_dict["misspell"]["enabled"]:
            if self.random.uniform(1,100) < self.settings_dict["misspell"]["frequencyPercentage"]:
                msg = misspell_word(message)
                misspelled = True
                # left off here!

        """
        TASK: remove repition here
        """
        if not self.command_handler_status["captcha"] or bypass:
            await self.wait_until_ready()
            if typingIndicator:
                async with channel.typing():
                    await channel.send(msg, silent=silent)
            else:
                await channel.send(msg, silent=silent)
            if not disable_log:
                await self.log(f"Ran: {msg}", color if color else "#5432a8")
            if misspelled:
                await self.set_stat(False, "misspell")
                time = self.calculate_correction_time(message)
                await self.log(f"correcting: {msg} -> {message} in {time}s", "#422052")
                await asyncio.sleep(time)
                if typingIndicator:
                    async with channel.typing():
                        await channel.send(message, silent=silent)
                else:
                    await channel.send(message, silent=silent)
                await self.set_stat(True, "misspell stop")

    async def slashCommandSender(self, msg, color, **kwargs):
        try:
            for command in self.slash_commands:
                if command.name == msg:
                    await self.wait_until_ready()
                    await command(**kwargs)
                    await self.log(f"Ran: /{msg}", color if color else "#5432a8")
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
        await asyncio.sleep(self.random.uniform(4.5, 6.4))
        await self.put_queue(
            {
                "cmd_name": self.alias["cash"]["normal"],
                "prefix": True,
                "checks": True,
                "id": "cash",
                "removed": False
            }
        )

    async def update_cash(self, amount, override=False, reduce=False, assumed=False):
        if override and self.settings_dict["cashCheck"]:
            self.user_status["balance"] = amount
        else:
            if self.settings_dict["cashCheck"] and not assumed:
                if reduce:
                    self.user_status["balance"] -= amount
                else:
                    self.user_status["balance"] += amount

            if reduce:
                self.user_status["net_earnings"] -= amount
            else:
                self.user_status["net_earnings"] += amount
        await self.update_cash_db()

    def get_nick(self, user):
        if user.nick:
            return user.nick
        elif user.display_name:
            return user.display_name
        else:
            return user.name


    async def setup_hook(self):
        # Randomise user

        if self.misc["debug"]["hideUser"]:
            x = [
                "Sunny", "River", "Echo", "Sky", "Shadow", "Nova", "Jelly", "Pixel",
                "Cloud", "Mint", "Flare", "Breeze", "Dusty", "Blip"
            ]
            random_part = self.random.choice(x)
            self.username = f"{random_part}_{abs(hash(str(self.user.id) + random_part)) % 10000}"
        else:
            self.username = self.user.name

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

        #self.nick_name = self.cm.guild.me.nick

        # self.dm = await (await self.fetch_user(self.owo_bot_id)).create_dm()
        # remove temp fix in `cogs/captcha.py` if uncommenting

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

        # Charts
        await self.populate_stats_db()

        await self.populate_cowoncy_earnings()
        await self.reset_gamble_wins_or_losses()

        await self.fetch_net_earnings()

        # Start various tasks and updates
        # self.config_update_checker.start()
        # disabled since unnecessory

        await asyncio.sleep(self.random_float(global_settings_dict["account"]["startupDelay"]))
        await self.update_config()

        if self.global_settings_dict["offlineStatus"]:
            self.presence.start()

        if self.settings_dict["sleep"]["enabled"]:
            self.random_sleep.start()

        if self.settings_dict["cashCheck"]:
            asyncio.create_task(self.check_for_cash())

def get_local_ip():
    if not global_settings_dict["website"]["enableHost"]:
        return 'localhost'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            """10.255.255.255 is fake"""
            s.connect(('10.255.255.255', 1))
            return s.getsockname()[0]
    except Exception:
        return 'localhost'


"""Handle Weekly runtime"""
def handle_weekly_runtime(path="utils/data/weekly_runtime.json"):
    while True:
        try:
            with open(path, "r") as config_file:
                weekly_runtime_dict = json.load(config_file)
            weekday = get_weekday()

            if weekly_runtime_dict[weekday][0] == 0:
                weekly_runtime_dict[weekday][0], weekly_runtime_dict[weekday][1] = time.time(), time.time()
            else:
                weekly_runtime_dict[weekday][1] = time.time()

            with open(path, "w") as f:
                json.dump(weekly_runtime_dict, f, indent=4)

        except Exception as e:
            print(f"Error when handling weekly runtime:\n{e}")

        # update every 15 seconds
        time.sleep(15)

def start_runtime_loop(path="utils/data/weekly_runtime.json"):
    try:
        with open(path, "r") as config_file:
            weekly_runtime_dict = json.load(config_file)

        now = time.time()
        last_checked = weekly_runtime_dict.get("last_checked", 0)

        if now - last_checked > 604800: # 604800 -> seconds in a week
            for day in map(str, range(7)):
                weekly_runtime_dict[day] = [0, 0]

        weekly_runtime_dict["last_checked"] = now

        with open(path, "w") as f:
            json.dump(weekly_runtime_dict, f, indent=4)

        loop_thread = threading.Thread(target=handle_weekly_runtime, daemon=True)
        loop_thread.start()

    except Exception as e:
        print(f"Error when attempting to start runtime handler:\n{e}")


"""Create SQLight database"""
def create_database(db_path="utils/data/db.sqlite"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(
        "CREATE TABLE IF NOT EXISTS commands (name TEXT PRIMARY KEY, count INTEGER)"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS cowoncy_earnings (user_id TEXT, hour INTEGER, earnings INTEGER, PRIMARY KEY (user_id, hour))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS gamble_winrate (hour INTEGER PRIMARY KEY, wins INTEGER, losses INTEGER, net INTEGER)"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS user_stats (user_id TEXT PRIMARY KEY, daily REAL, lottery REAL, cookie REAL, giveaways REAL, captchas INTEGER, cowoncy INTEGER)"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS meta_data (key TEXT PRIMARY KEY, value INTEGER)"
    )
    # Switch to WAL mode.
    c.execute("PRAGMA journal_mode=WAL;")

    # Populate

    # -- gamble_winrate
    for hr in range(24):
        # hour does not have 24 in 24 hr format!!
        c.execute("INSERT OR IGNORE INTO gamble_winrate (hour, wins, losses, net) VALUES (?, ?, ?, ?)", (hr, 0, 0, 0))

    # -- meta data
    c.execute("INSERT OR IGNORE INTO meta_data (key, value) VALUES (?, ?)", ("gamble_winrate_last_checked", 0))
    c.execute("INSERT OR IGNORE INTO meta_data (key, value) VALUES (?, ?)", ("cowoncy_earnings_last_checked", 0))

    # -- commands
    for cmd in misc_dict["command_info"].keys():
        c.execute("INSERT OR IGNORE INTO commands (name, count) VALUES (?, ?)", (cmd, 0))

    # -- end --#
    conn.commit()
    conn.close()


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
        thread = Thread(target=run_bot, args=(token, channel_id, global_settings_dict))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def run_bot(token, channel_id, global_settings_dict):
    try:
        logging.getLogger("discord.client").setLevel(logging.ERROR)
        client = MyClient(token, channel_id, global_settings_dict)

        if not on_mobile:
            try:
                client.run(token, log_level=logging.ERROR)

            except CurlError as e:
                if "WS_SEND" in str(e) and "55" in str(e):
                    printBox("Broken pipe error detected. Restarting bot...", "bold red")
                    # add a restart of client.run after exiting cleanly here!
                else:
                    printBox(f"Curl error: {e}", "bold red")
        else:
            client.run(token, log_level=logging.ERROR)

    except Exception as e:
        printBox(f"Error starting bot: {e}", "bold red")

def run_bot(token, channel_id, global_settings_dict):
    try:
        logging.getLogger("discord.client").setLevel(logging.ERROR)

        while True:
            client = MyClient(token, channel_id, global_settings_dict)

            if not on_mobile:
                try:
                    client.run(token, log_level=logging.ERROR)

                except CurlError as e:
                    if "WS_SEND" in str(e) and "55" in str(e):
                        printBox("Broken pipe error detected. Restarting bot...", "bold red")
                        # Restart the loop with a new client instance.
                        continue 
                    else:
                        printBox(f"Curl error: {e}", "bold red")
                        # Don't retry unknown curl errors.
                        break 
                except Exception as e:
                    printBox(f"Unknown error when running bot: {e}", "bold red")

            else:
                # Mobile (Termux) uses an older version without curl_cffi.
                # No need to handle error in such cases.
                try:
                    client.run(token, log_level=logging.ERROR)
                except Exception as e:
                    printBox(f"Unknown error when running bot: {e}", "bold red")
                break 

    except Exception as e:
        printBox(f"Error starting bot: {e}", "bold red")

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

if __name__ == "__main__":
    try:
        discord_cur_version = import_ver("discord.py-self")
        discord_req_version = "2.1.0a5097+g20ae80b3"
        if discord_cur_version != discord_req_version:
            install_package("git+https://github.com/dolfies/discord.py-self@20ae80b398ec83fa272f0a96812140e14868c88f")
            raise SystemExit("discord.py-self was reinstalled. Please restart the program.")
    except ImportError as e:
        print(e)

    if not misc_dict["console"]["compactMode"]:
        console.print(owoPanel)
        console.rule(f"[bold blue1]version - {version}", style="navy_blue")
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

    # Create database or modify if required
    create_database()

    # Weekly runtime thread
    start_runtime_loop()

    if global_settings_dict["website"]["enabled"]:
        # Start website
        web_thread = threading.Thread(target=web_start)
        web_thread.start()
        # get ip
        ip = get_local_ip()
        printBox(f'Website Dashboard: http://{ip}:{global_settings_dict["website"]["port"]}'.center(console_width - 2 ), 'dark_magenta')
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
        print(f"Error - {e}, while attempting to fetch news")

    if not misc_dict["console"]["hideStarRepoMessage"]:
        console.print("Star the repo in our github page if you want us to continue maintaining this proj :>.", style = "thistle1")
    console.rule(style="navy_blue")


    if not on_mobile:
        # To catch `Broken pipe` error
        from curl_cffi.curl import CurlError
    
    if global_settings_dict["captcha"]["toastOrPopup"] and not on_mobile and not misc_dict["hostMode"]:
        try:
            import tkinter as tk
            from tkinter import PhotoImage
            from queue import Queue
        except Exception as e:
            print(f"ImportError: {e}")
            
        popup_queue = Queue()

        bot_threads = threading.Thread(target=run_bots, args=(tokens_and_channels,))
        bot_threads.daemon = True
        bot_threads.start()

        popup_main_loop()
    else:
        run_bots(tokens_and_channels)
