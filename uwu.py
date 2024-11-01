"""
NOTE:
This repo is made with the help of https://github.com/BridgeSenseDev/Dank-Memer-Grinder
So there are many parts I don't understand properly yet.
To make it easier to maintain ill be adding lots of comments,
Please don't remove those if making contributions!
"""
# Do consider giving our repo a star in github :>

from discord.ext import commands
from rich.console import Console
from threading import Thread
from rich.panel import Panel
from rich.align import Align
import discord
import asyncio
import logging
import random
import aiohttp
import json
import sys
import os


def clear():
    os.system('cls') if os.name == 'nt' else os.system('clear')

console = Console()

clear()

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

console.rule("[bold blue1]:>", style="navy_blue")
console_width = console.size.width
listUserIds = []

owoArt = r"""
  __   _  _   __       ____  _  _  ____  __ _ 
 /  \ / )( \ /  \  ___(    \/ )( \/ ___)(  / )
(  O )\ /\ /(  O )(___)) D () \/ (\___ \ )  ( 
 \__/ (_/\_) \__/     (____/\____/(____/(__\_)
"""
owoPanel = Panel(Align.center(owoArt), style="purple on black", highlight=False)
version = "2.0.0-alpha"
debug_print = True

def printBox(text, color):
    test_panel = Panel(text, style=color)
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
        
    def random_float(self, cooldown_list):
        return random.uniform(cooldown_list[0],cooldown_list[1])

    def log(self, text, color, bold=False, debug=debug_print):
        style = f"{color} on black"
        if debug:
            console.log(text, style=style)
        else:
            console.print(text.center(console_width - 2), style=style)

    async def on_ready(self):
        self.on_ready_dn = False
        self.cmds = 1
        self.owo_bot_id = 408785106942164992
        if self.session is None:
            self.session = aiohttp.ClientSession()
        await asyncio.sleep(0.1)
        printBox(f'-Loaded {self.user.name}[*].'.center(console_width - 2 ),'bold royal_blue1 on black' )
        listUserIds.append(self.user.id)
        # Load cogs
        
        for filename in os.listdir(resource_path("./cogs")):
            if filename.endswith(".py"):
                print(filename)
                await self.load_extension(f"cogs.{filename[:-3]}")
        #self.log(f'{self.user}[+] ran hunt', 'purple')

        try:
            self.cm = self.get_channel(self.channel_id)
        except Exception as e:
            print(e)
        """
        NOTE:-  Temporary fix for https://github.com/dolfies/discord.py-self/issues/744
        Hopefully the above gets fixed soon.
        for now we will send `owo ping` command in the grind channel to get owo bot's message through the channels history.
        then we will use that instead to create the dm
        """
        try:
            self.dm = await (await self.fetch_user(self.owo_bot_id)).create_dm()
            print(self.dm)
        except discord.Forbidden as e:
            print(e)
            print(f"attempting to get user with the help of {self.cm}")
            await self.cm.send(f"{config_dict["setprefix"]}ping")
            print(f"{self.user} send ping command to trigger bot response")
            async for message in self.cm.history(limit=10):
                if message.author.id == self.owo_bot_id:
                    print(f"{self.user} found bot!, attempting to create dm")
                    break
            await asyncio.sleep(random.uniform(0.5,0.9))
            self.dm = await message.author.create_dm()
            print(f"{self.user} created dm {self.dm} successfully!")
            #print(self.dm)
        except Exception as e:
            print(e)

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
    console.rule(style="navy_blue")
    printBox(f'-Made by EchoQuill'.center(console_width - 2 ),'bold grey30 on black' )
    printBox(f'-Current Version:- {version}'.center(console_width - 2 ),'bold spring_green4 on black' )
    tokens_and_channels = [line.strip().split() for line in open("tokens.txt", "r")]
    token_len = len(tokens_and_channels)
    printBox(f'-Recieved {token_len} tokens.'.center(console_width - 2 ),'bold magenta on black' )
    console.print("Star the repo in our github page if you want us to continue maintaining this proj :>.", style = "thistle1 on black")
    console.rule(style="navy_blue")
    run_bots(tokens_and_channels)
