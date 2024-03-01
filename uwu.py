from colorama import Fore, Back, init as colorama_init
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord import SyncWebhook
from threading import Thread
import discord.errors
import requests
import random
import secrets
import discord
import asyncio
import logging
import time
import json
import sys
import os

# Random module seed
seed = secrets.randbelow(1184746474747)
random.seed(seed)


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

with open(resource_path("config.json")) as file:
    config = json.load(file)

replied_adv_messages = {}
webhookEnabled = config["webhookEnabled"]
termuxNotificationEnabled = config["termuxAntiCaptchaSupport"]["notifications"]
termuxVibrationEnabled = config["termuxAntiCaptchaSupport"]["vibrate"]["enabled"]
termuxVibrationTime = config["termuxAntiCaptchaSupport"]["vibrate"]["time"] * 1000
termuxTtsEnabled = config["termuxAntiCaptchaSupport"]["texttospeech"]["enabled"]
termuxTtsContent = config["termuxAntiCaptchaSupport"]["texttospeech"]["content"]
mobileBatteryCheckEnabled = config["termuxAntiCaptchaSupport"]["batteryCheck"]["enabled"]
mobileBatteryStopLimit = config["termuxAntiCaptchaSupport"]["batteryCheck"]["percentage"]
desktopNotificationEnabled = config["desktopNotificationEnabled"]
autoHunt = config["commands"][0]["hunt"]
autoBattle = config["commands"][1]["battle"]
autoPray = config["commands"][2]["pray"]
usertopray = config["commands"][2]["usertopray"]
autoCurse = config["commands"][3]["curse"]
usertocurse = config["commands"][3]["usertocurse"]
autoDaily = config["autoDaily"]
setprefix = config["setprefix"]
webhook_url = config["webhook"]
list_captcha = ["captcha","link below","https://owobot.com/captcha","letter","verification test"]

class MyClient(discord.Client):
    def __init__(self, token, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = int(channel_id)
        self.list_channel = [self.channel_id] 
    @tasks.loop()
    async def send_daily(self):
        if self.justStarted:
            await asyncio.sleep(random.uniform(21,67))
            await self.cm.send(f"{setprefix}daily")
            self.lastcmd = "daily"
        while self.busy:
            await asyncio.sleep(random.uniform(10,30))
        self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
        self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst

        self.formatted_time = "{:02}h {:02}m {:02}s".format(
            int(self.time_until_12am_pst.total_seconds() // 3600),
            int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
            int(self.time_until_12am_pst.total_seconds() % 60)
)
        self.total_seconds = self.time_until_12am_pst.total_seconds()
        print(f"Time till mext daily for {self.user.name} = {self.formatted_time}")
        while self.busy:
            await asyncio.sleep(random.uniform(10,30))
        self.busy = True
        await asyncio.sleep(self.total_seconds+random.uniform(30,90))
        await self.cm.send(f"{setprefix}daily")
        self.lastcmd = "daily"

    @tasks.loop()
    async def send_hunt(self):
        if self.f != True:
            self.ranint = random.randint(1,5)
            if self.ranint <= 2: 
                if self.busy:
                    await asyncio.sleep(random.uniform(0.6367373,0.98383737))
                    await self.cm.send(f'{setprefix}h')
                    self.lastcmd = "hunt"
                    self.busy = True
                    await asyncio.sleep(random.uniform(11.6,13.9))
                else:
                    await self.cm.send(f'{setprefix}h')
                    self.lastcmd = "hunt"
                    self.busy = True
                    await asyncio.sleep(random.uniform(11.6,13.9)) 
            else:
                if self.busy:
                    await asyncio.sleep(random.uniform(0.6367373,0.98383737))
                    await self.cm.send(f'{setprefix}h')
                    self.lastcmd = "hunt"
                    self.busy = True
                    await asyncio.sleep(random.uniform(14.99, 15.10))
                else:
                    await self.cm.send(f'{setprefix}h')
                    self.lastcmd = "hunt"
                    self.busy = True
                    await asyncio.sleep(random.uniform(14.99, 15.10))
            print(f'{Fore.LIGHTYELLOW_EX}[0|{self.user}] {Fore.LIGHTRED_EX}hunt')

    @tasks.loop()
    async def send_battle(self):
        if self.f != True:
            if self.justStarted:
                await asyncio.sleep(random.uniform(1.837,1.9998))
                await self.cm.send(f'{setprefix}b')
                self.busy = True
                self.lastcmd = "battle"
                await asyncio.sleep(random.uniform(14.99, 15.10))
            else:
                self.ranint = random.randint(1,5)
                if self.ranint <= 2: 
                    if self.busy:
                        await asyncio.sleep(random.uniform(0.6367373,0.98383737))
                        await self.cm.send(f'{setprefix}b')
                        self.lastcmd = "battle"
                        self.busy = True
                        await asyncio.sleep(random.uniform(11.6,13.9))
                    else:
                        await self.cm.send(f'{setprefix}b')
                        self.lastcmd = "battle"
                        self.busy = True
                        await asyncio.sleep(random.uniform(11.6,13.9)) 
                else:
                    if self.busy:
                        await asyncio.sleep(random.uniform(0.6367373,0.98383737))
                        await self.cm.send(f'{setprefix}b')
                        self.lastcmd = "battle"
                        self.busy = True
                        await asyncio.sleep(random.uniform(14.99, 15.10))
                    else:
                        await self.cm.send(f'{setprefix}b')
                        self.lastcmd = "battle"
                        self.busy = True
                        await asyncio.sleep(random.uniform(14.99, 15.10))
            print(f'{Fore.LIGHTYELLOW_EX}[0|{self.user}] {Fore.LIGHTRED_EX}battle')

    @tasks.loop()
    async def send_curse(self):
        if self.justStarted:
            await asyncio.sleep(random.uniform(0.93535353, 1.726364646))
        if self.busy:
            await asyncio.sleep(random.uniform(0.63535353, 0.726364646))
        if self.f != True:
            if usertopray:
                await self.cm.send(f'{setprefix}curse <@{usertopray}>')
                self.lastcmd = "curse"
            else:
                await self.cm.send(f'{setprefix}curse')
                self.lastcmd = "curse"
            print(f'{Fore.LIGHTYELLOW_EX}[0|{self.user}] {Fore.LIGHTMAGENTA_EX}curse')
            await asyncio.sleep(random.uniform(300.73635374263,310.4969684))

    @tasks.loop()
    async def send_prayer(self):
        if self.justStarted:
            await asyncio.sleep(random.uniform(0.93535353, 1.726364646))
        if self.busy:
            await asyncio.sleep(random.uniform(0.63535353, 0.726364646))
        if self.f != True:
            if usertopray:
                await self.cm.send(f'{setprefix}pray <@{usertopray}>')
                self.lastcmd = "pray"
            else:
                await self.cm.send(f'{setprefix}pray')
                self.lastcmd = "pray"
            print(f'{Fore.LIGHTYELLOW_EX}[0|{self.user}] {Fore.LIGHTMAGENTA_EX}pray')
            await asyncio.sleep(random.uniform(300.73635377263,310.5969684))

    async def on_ready(self):
        self.on_ready_dn = False
        self.cmds = 1
        self.cmds_cooldown = 0
        await asyncio.sleep(1)
        print(f'{Fore.LIGHTGREEN_EX}________________________________')
        print(f'-{Fore.GREEN}Loaded{Fore.YELLOW} {self.user.name}.')
        print(f'{Fore.LIGHTGREEN_EX}________________________________')
        await asyncio.sleep(0.12)
        self.cm = self.get_channel(self.channel_id)
        self.dm = await self.fetch_user(408785106942164992)
        self.list_channel.append(self.dm.dm_channel.id)
        self.hunt = None
        self.battle = None
        self.justStarted = True
        self.list_channel = [self.channel_id, self.dm.dm_channel.id]
        print(self.dm.dm_channel.id)
        self.spams = 0
        self.lastcmd = None
        self.busy = False
        self.f = False
        await asyncio.sleep(0.6)
        if autoHunt:
            self.send_hunt.start()
        if autoBattle:
            self.send_battle.start()
        if autoCurse:
            self.send_curse.start()
        if autoPray:
            self.send_prayer.start()
        if autoDaily:
            self.send_daily.start()

        embed1 = discord.Embed(
            title='logging in',
            description=f'logged in as {self.user.name}',
            color=discord.Color.dark_green()
        )

        self.webhook = SyncWebhook.from_url(webhook_url)
        if webhookEnabled:
            self.webhook.send(embed=embed1, username='uwu bot') 
        await asyncio.sleep(random.uniform(2.69,3.69))
        if desktopNotificationEnabled:
            pass
        self.justStarted = False

    async def on_message(self, message):
        if not self.is_ready():
            return
        if message.author.id != 408785106942164992:
            return
        if any(b in message.content.lower() for b in list_captcha) and message.channel.id in self.list_channel:
            self.f = True
            if termuxNotificationEnabled:
                os.system("termux-notification -c 'captcha detected!'")
                os.system("termux-toast -c red -b black 'Captcha Detected please solve'")
            print("unsolved captcha!!!!, stopping")   
            embed2 = discord.Embed(
                    title=f'CAPTCHA :- {self.user} ;<',
                    description=f"user got captcha :- {self.user} ;<",
                    color=discord.Color.red()
                                )
            if webhookEnabled:
                self.webhook.send(embed=embed2, username='uwu bot warnings')
            if termuxVibrationEnabled:
                os.system(f"termux-vibrate -d {termuxVibrationTime}")
            if termuxTtsEnabled:
                os.system(f"termux-tts-speak {termuxTtsContent}")
            return
        if message.channel.id == self.channel_id and "please slow down~ you're a little **too fast** for me :c" in message.content.lower():
            print("hitting cds")
            #content.
            self.spams+=1
        if message.channel.id == self.channel_id and "slow down and try the command again" in message.content.lower():
            await asyncio.sleep(random.uniform(3.9,5.2))
            if self.lastcmd == "hunt":
                await self.cm.send(f"{setprefix}h")
            if self.lastcmd == "battle":
                await self.cm.send(f"{setprefix}b")
        if message.channel.id == self.channel_id and ('you found' in message.content.lower() or "caught" in message.content.lower()):
            if self.lastcmd == "hunt":
                await asyncio.sleep(random.uniform(0.7,0.9))
                self.busy = False #crate | kira, You found a weapon crate! [3/3] RESETS IN: 3H 15M 23S
        if message.channel.id == self.channel_id and ("you found a **lootbox**!" in message.content.lower() or "you found a **weapon crate**!" in message.content.lower()):
            if "**lootbox**" in message.content.lower():
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.busy = True
                await self.cm.send(f"{setprefix}lb all")
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.busy = False
            elif "**weapon crate**" in message.content.lower():
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.busy = True
                await self.cm.send(f"{setprefix}crate all")
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.busy = False
        if message.embeds and message.channel.id == self.channel_id:
            for embed in message.embeds:
                if embed.author.name is not None and "goes into battle!" in embed.author.name.lower():
                  #  print("battle works (1)")
                    if self.lastcmd == "battle":
                    #    print("battle works (2)")
                        await asyncio.sleep(random.uniform(0.7,0.9))
                        self.busy = False

def run_bots(tokens_and_channels):
    threads = []
    for token, channel_id in tokens_and_channels:
        thread = Thread(target=run_bot, args=(token, channel_id))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
def run_bot(token, channel_id):
    client = MyClient(token, channel_id)
    client.run(token)
if __name__ == "__main__":
    colorama_init(autoreset=True)
    print(f'''{Fore.LIGHTCYAN_EX}
 _          __      _         
/ \     _  (_  _ |_|_|_  __|_ 
\_/\/\/(_) __)(/_| | |_)(_)|_ 
''')
    print() 
    if autoPray == True and autoCurse == True:
        print(f'{Fore.RED}error, both auto pray and auto curse are enabled at the same time, please disable one and restart the code')
    if autoHunt == False and autoBattle == False:
        print(f'{Fore.RED}starting without autoHunt and autoBattle')
    if termuxNotificationEnabled and desktopNotificationEnabled:
        print(f"{Fore.RED}can't enable both desktop and termux notifications at the same time in variables.")
    
    tokens_and_channels = [line.strip().split() for line in open("toke.txt", "r")]
    print(f'{Fore.GREEN}Loaded {len(tokens_and_channels)} tokens and channel IDs.')
    print(f'{Fore.YELLOW} current seed = {seed}')
    logging.basicConfig(level=logging.WARNING)
    run_bots(tokens_and_channels)
