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
import asyncio
import logging
import aiohttp
import sys
import os

def clear():
    os.system('cls') if os.name == 'nt' else os.system('clear')

console = Console()

clear()

console.rule("[bold blue1]:>", style="white")
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
        console.rule(style="white")
    
    def log(self, text, color, bold=False, debug=debug_print):
        style = f"{color} on black" if not bold else f"bold {color} on black"
        if debug:
            console.log(text, style=style)
        else:
            console.print(text.center(console_width - 2), style=style)

    async def on_ready(self):
        self.on_ready_dn = False
        self.cmds = 1
        if self.session is None:
            self.session = aiohttp.ClientSession()
        await asyncio.sleep(0.1)
        printBox(f'-Loaded {self.user.name}[*].'.center(console_width - 2 ),'bold purple on black' )
        listUserIds.append(self.user.id)
        # Load cogs
        
        for filename in os.listdir(resource_path("./cogs")):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        console.print(f'{self.user}[+] ran hunt'.center(console_width - 2 ),style='bold purple on black')
        self.log(f'{self.user}[+] ran hunt', 'purple')

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
    console.rule(style="white")
    printBox(f'-Made by EchoQuill'.center(console_width - 2 ),'bold grey30 on black' )
    printBox(f'-Current Version:- {version}'.center(console_width - 2 ),'bold spring_green4 on black' )
    tokens_and_channels = [line.strip().split() for line in open("tokens.txt", "r")]
    token_len = len(tokens_and_channels)
    printBox(f'-Recieved {token_len} tokens.'.center(console_width - 2 ),'bold magenta on black' )
    console.print("Star the repo in our github page if you want us to continue maintaining this proj :>.", style = "thistle1 on black")
    run_bots(tokens_and_channels)
