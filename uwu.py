# Do consider giving our repo a star in github :>

from datetime import datetime, timedelta, timezone
from discord.ext import commands
from rich.console import Console
from threading import Thread
from rich.panel import Panel
from rich.align import Align
from queue import Queue
import discord
import asyncio
import logging
import random
import traceback
import threading
import aiohttp
import json
import pytz
import sys
import os
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
        self.queue = Queue()



        
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
        print(data, "   - construct_command")
        prefix = config_dict['setprefix'] if data.get("prefix") else ""
        return f"{prefix}{data['cmd_name']} {data.get('cmd_arguments', '')}".strip()


    def put_queue(self, cmd_data):
        #print(f"{config_dict['setprefix']}{cmd}" if prefix else cmd, check)
        self.queue.put(cmd_data)
    
    def remove_queue(self, cmd_data, **kwargs):
        self.checks = [
            check for check in self.checks 
            if check[0] != cmd_data
        ]



    def log(self, text, color, bold=False, debug=debug_print):
        style = f"{color} on black"
        if debug:
            #frame_info = traceback.extract_stack()[-2]
            #print(frame_info)
            #print(f"{frame_info.filename}, {frame_info.lineno}")
            console.log(text, style=style) # stack_offset changes the line no to the place where log func was called.
        else:
            console.print(text.center(console_width - 2), style=style)


    # send commands
    async def send(self, message, bypass=False, channel=None, silent=config_dict["silentTextMessages"], typingIndicator=config_dict["typingIndicator"]):
        if not channel:
            channel = self.cm
        if not self.captcha and (self.state or bypass):
            if typingIndicator:
                async with channel.typing():
                    await channel.send(message, silent=silent)
            else:
                await channel.send(message, silent=silent)

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
            print(f"attempting to get channel {self.channel_id}")
            self.cm = self.get_channel(self.channel_id)
            print(self.cm)
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
            print(self.dm)
        except discord.Forbidden as e:
            print(e)
            print(f"attempting to get user with the help of {self.cm}")
            await self.cm.send(f"{config_dict['setprefix']}ping")
            print(f"{self.user} send ping command to trigger bot response")
            async for message in self.cm.history(limit=10):
                if message.author.id == self.owo_bot_id:
                    print(f"{self.user} found bot!, attempting to create dm")
                    break
            await asyncio.sleep(random.uniform(0.5,0.9))
            self.dm = await message.author.create_dm()
            print(f"{self.user} created dm {self.dm} successfully!")
            print(self.dm)
        except Exception as e:
            print(e)

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
            print(accounts_dict)
            if str(self.user.id) not in accounts_dict:
                accounts_dict.update(self.default_config)
                with open("utils/stats.json", "w") as f:
                    json.dump(accounts_dict, f, indent=4)
                accounts_dict = load_accounts_dict()

                print(f"Default values added for bot ID: {self.user.id}")
            else:
                print("Bot ID already exists in accounts.json.")

        # Load cogs
        for filename in os.listdir(resource_path("./cogs")):
            if filename.endswith(".py"):
                print(filename)
                await self.load_extension(f"cogs.{filename[:-3]}")
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
    logging.getLogger("discord.client").setLevel(logging.INFO)
    client = MyClient(token, channel_id)
    client.run(token, log_level=logging.INFO)
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
