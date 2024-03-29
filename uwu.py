# Iam obsessed with imports being in descending order.
# Written by EchoQuill, on a laggy mobile that too.
# Make sure to star the github page.
#------------------------------------------------
# REMINDER:- THIS IS MOSTLY MADE FOR MOBILE
# it might look ugly in desktop consoles etc.
# iam bad with decorating cli
#------------------------------------------------
# It would also be great if you understand that iam a new python developer
# Iam not that skilled so there might be some repetitions etc
# Please do give me pointers on how to improve.
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord import SyncWebhook
from rich.console import Console
from threading import Thread
from rich.panel import Panel
import discord.errors
import requests
import random
import secrets
import discord
import asyncio
import logging
import string
import shutil
import time
import json
import sys
import os
import re
os.system("clear")
# For console.log thingy
console = Console()
# Random module seed for better anti detection.
seed = secrets.randbelow(4765839360747)
random.seed(seed)
# Console width size
console_width = shutil.get_terminal_size().columns
# Owo text art for panel 
owoArt = """
 _          __      _         
/ \     _  (_  _ |_|_|_  __|_ 
\_/\/\/(_) __)(/_| | |_)(_)|_ 
"""
owoPanel = Panel(owoArt, style="purple on black", highlight=False)

# Load json file
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
with open(resource_path("config.json")) as file:
    config = json.load(file)

#----------OTHER VARIABLES----------#
list_captcha = ["captcha","link below","https://owobot.com/captcha","letter","verification test"]
mobileBatteryCheckEnabled = config["termuxAntiCaptchaSupport"]["batteryCheck"]["enabled"]
mobileBatteryStopLimit = config["termuxAntiCaptchaSupport"]["batteryCheck"]["percentage"]
termuxNotificationEnabled = config["termuxAntiCaptchaSupport"]["notifications"]
termuxTtsEnabled = config["termuxAntiCaptchaSupport"]["texttospeech"]["enabled"]
termuxTtsContent = config["termuxAntiCaptchaSupport"]["texttospeech"]["content"]
termuxVibrationEnabled = config["termuxAntiCaptchaSupport"]["vibrate"]["enabled"]
termuxVibrationTime = config["termuxAntiCaptchaSupport"]["vibrate"]["time"] * 1000
desktopNotificationEnabled = config["desktopNotificationEnabled"]
webhookEnabled = config["webhookEnabled"]
webhook_url = config["webhook"]
setprefix = config["setprefix"]

#----------MAIN VARIABLES----------#
listUserIds = []
autoHunt = config["commands"][0]["hunt"]
autoBattle = config["commands"][0]["battle"]
autoPray = config["commands"][1]["pray"]
autoCurse = config["commands"][1]["curse"]
userToPrayOrCurse = config["commands"][1]["userToPrayOrCurse"]
autoDaily = config["autoDaily"]
autoOwo = config["sendOwo"]
autoCrate = config["autoUse"]["autoUseCrate"]
autoLootbox = config["autoUse"]["autoUseLootbox"]
autoHuntGem = config["autoUse"]["autoGem"]["huntGem"]
autoEmpoweredGem = config["autoUse"]["autoGem"]["empoweredGem"]
autoLuckyGem = config["autoUse"]["autoGem"]["luckyGem"]
autoSpecialGem = config["autoUse"]["autoGem"]["specialGem"]
autoSell = config["commands"][2]["sell"]
autoSac = config["commands"][2]["sacrifice"]
autoQuest = config["commands"][6]["quest"]
ignoreDisable_Quest = config["commands"][6]["doEvenIfDisabled"]
rarity = ""
for i in config["commands"][2]["rarity"]:
    rarity + i + " "
autoCf = config["commands"][4]["coinflip"]
cfAmt = config["commands"][4]["startValue"]
cfAllotedValue = config["commands"][4]["allottedAmount"]
autoSlots = config["commands"][3]["slots"]
slotsAmt = config["commands"][3]["startValue"]
slotsCooldown = config["commands"][3]["cooldown"]
slotsAllotedValue = config["commands"][3]["allottedAmount"]
customCommands = config["customCommands"]["enabled"]
commandsList = config["customCommands"]["commands"]
commandsCooldown = config["customCommands"]["cooldowns"]
lottery = config["commands"][7]["lottery"]
lotteryAmt = config["commands"][7]["amount"]
lvlGrind = config["commands"][8]["lvlGrind"]
#dble check
sorted_pairs = sorted(zip(commandsList, commandsCooldown))
sorted_list1 = [pair[1] for pair in sorted_pairs]
#lotter amt check:-
if lotteryAmt > 250000:
    lotteryAmt = 250000
# Gems.
huntGems = [57,56,55,54,53,52,51]
empGems = [71,70,69,68,67,66,65]
luckGems = [78,77,76,75,74,73,72]
specialGems = [85,84,83,82,81,80,79]
qtemp = []
# Cooldowns
huntOrBattleCooldown = config["commands"][0]["cooldown"]
prayOrCurseCooldown = config["commands"][1]["cooldown"]
sellOrSacCooldown = config["commands"][2]["cooldown"]
slotsCooldown = config["commands"][3]["cooldown"]
cfCooldown = config["commands"][4]["cooldown"]
lvlGrindCooldown = config["commands"][8]["cooldown"]

# Box print
def printBox(text, color):
    test_panel = Panel(text, style=color)
    console.print(test_panel)
# For lvl grind
def generate_random_string():
    characters = string.ascii_lowercase + ' '
    length = random.randint(5, 20)
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string
    
class MyClient(discord.Client):
    def __init__(self, token, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = int(channel_id)
        self.list_channel = [self.channel_id]   
#----------SENDING COMMANDS----------#
    #daily
    @tasks.loop()
    async def send_daily(self):
        if self.justStarted:
            await asyncio.sleep(random.uniform(21,67))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
            await self.cm.send(f"{setprefix}daily")
            self.last_cmd_time = time.time()
            self.lastcmd = "daily"
        self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
        self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst
        
        self.formatted_time = "{:02}h {:02}m {:02}s".format(
            int(self.time_until_12am_pst.total_seconds() // 3600),
            int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
            int(self.time_until_12am_pst.total_seconds() % 60)
)
        self.total_seconds = self.time_until_12am_pst.total_seconds()
        #print(f"Time till mext daily for {self.user.name} = {self.formatted_time}")
        console.print(f"-{self.user}[+] ran daily (next daily :> {self.formatted_time})".center(console_width - 2 ), style = "Cyan on black")
        await asyncio.sleep(self.total_seconds+random.uniform(30,90))
        self.current_time = time.time()
        self.time_since_last_cmd = self.urrent_time - self.last_cmd_time
        if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
            await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
        await self.cm.send(f"{setprefix}daily")
        self.lastcmd = "daily"
        
    #hunt/daily
    @tasks.loop()
    async def send_hunt_or_battle(self):
        #print(self.hb)
        if not self.huntOrBattleSelected:
            if self.hb == 1:
                self.huntOrBattle = "battle"
            elif self.hb == 0:
                self.huntOrBattle = "hunt"
        if self.f != True:
            self.current_time = time.time()
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
            else:
                pass
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            await self.cm.send(f'{setprefix}{self.huntOrBattle}')
            console.print(f"-{self.user}[+] ran {self.huntOrBattle}.".center(console_width - 2 ), style = "purple on black")
            if self.hb == 1:
                await asyncio.sleep(huntOrBattleCooldown + random.uniform(0.99, 1.10))
    #pray/curse
    @tasks.loop()
    async def send_curse_and_prayer(self):
        if self.justStarted:
            await asyncio.sleep(random.uniform(0.93535353, 1.726364646))
        if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
            await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))        
        if self.f != True:
            if userToPrayOrCurse and self.user.id != userToPrayOrCurse:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                await self.cm.send(f'{setprefix}{self.prayOrCurse} <@{userToPrayOrCurse}>')
                self.lastcmd = self.prayOrCurse
                self.last_cmd_time = time.time()
            else:
                await self.cm.send(f'{setprefix}{self.prayOrCurse}')
                self.lastcmd = self.prayOrCurse
                self.last_cmd_time = time.time()
            console.print(f"-{self.user}[+] ran {self.prayOrCurse}.".center(console_width - 2 ), style = "magenta on black")
            await asyncio.sleep(prayOrCurseCooldown + random.uniform(0.99, 1.10))
     #coinflip
    @tasks.loop()
    async def send_cf(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.cfAmt*self.cfN > 250000:
                console.print(f"-{self.user}[-] Stopping coin flip [250k exceeded]".center(console_width - 2 ), style = "red on black")
                self.send_cf.stop()
            elif self.cfAllotedValue < self.cft:
                console.print(f"-{self.user}[-] Stopping coin flip [allotted value exceeded]".center(console_width - 2 ), style = "red on black")
                self.send_cf.stop()
            await self.cm.send(f'{setprefix}cf {self.cfAmt*self.cfN}')
            await asyncio.sleep(cfCooldown + random.uniform(0.28288282, 0.928292929))
   # Slots
    @tasks.loop()
    async def send_slots(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.slotsAmt*self.zlotsN > 250000:
                console.print(f"-{self.user}[-] Stopping slots [250k exceeded]".center(console_width - 2 ), style = "red on black")
                self.send_slots.stop()
            elif self.slotsAllotedValue < self.slotsT:
                console.print(f"-{self.user}[-] Stopping slots [allotted value exceeded]".center(console_width - 2 ), style = "red on black")
                self.send_slots.stop()
            await self.cm.send(f'{setprefix}slots {slotsAmt*slotsN}')
            console.print(f"-{self.user}[+] ran Coinflip.".center(console_width - 2 ), style = "cyan on black")
            await asyncio.sleep(slotsCooldown + random.uniform(0.28288282, 0.928292929))
     # Owo top
    @tasks.loop()
    async def send_owo(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            await self.cm.send('owo')
            console.print(f"-{self.user}[+] ran owo".center(console_width - 2 ), style = "Cyan on black")
            if autoOwo == False:
                self.owoTempInt+=1 
                if self.owoTempInt == self.owoTempIntTwo:
                    self.send_owo.stop()
            await asyncio.sleep(random.uniform(19.28288282, 21.928292929))
    # auto sell / auto sac.
    @tasks.loop()
    async def send_sell_or_sac(self):
        #print(self.hb)
        if not self.sellOrSacSelected:
            if self.ss == 1:
                self.sellOrSac = "sac"
                self.ss = 0
            elif self.ss == 0:
                self.sellOrSac = "sell"
                self.ss = 1
        if self.f != True:
            self.current_time = time.time()
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                await self.cm.send(f'{setprefix}{self.sellOrSac} {rarity}')
                self.last_cmd_time = time.time()
                console.print(f"-{self.user}[+] ran {self.sellOrSac}".center(console_width - 2 ), style = "Cyan on black")
                await asyncio.sleep(sellOrSacCooldown + random.uniform(0.377373, 1.7373828))
     # Custom commands
    @tasks.loop()
    async def send_custom(self):
        if self.f != True:
            self.index = 0
            for i in commandsList:
                await asyncio.sleep(random.uniform(commandsCooldown[self.index] + 0.3, commandsCooldown[self.index] + 0.5))
                self.index+=1
                await self.cm.send(i)
                self.last_cmd_time = time.time()
    # Quests
    @tasks.loop()
    async def check_quests(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            await self.cm.send(f'{setprefix}quest')
            self.qtemp2 = False
            console.print(f"-{self.user}[+] checking quest status...".center(console_width - 2 ), style = "magenta on black")
            await asyncio.sleep(random.uniform(500.28288282, 701.928292929))
            if self.qtemp:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
                self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst       
                self.formatted_time = "{:02}h {:02}m {:02}s".format(
                    int(self.time_until_12am_pst.total_seconds() // 3600),
                    int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
                    int(self.time_until_12am_pst.total_seconds() % 60)
            )
                self.total_seconds = self.time_until_12am_pst.total_seconds()
                await asyncio.sleep(self.total_seconds + random.uniform(34.377337,93.7473737))
    # Lottery
    @tasks.loop()
    async def send_lottery(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
            self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst       
            self.formatted_time = "{:02}h {:02}m {:02}s".format(
                int(self.time_until_12am_pst.total_seconds() // 3600),
                int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
                int(self.time_until_12am_pst.total_seconds() % 60)
        )
            self.total_seconds = self.time_until_12am_pst.total_seconds()
            await self.cm.send(f'{setprefix}lottery {self.lotteryAmt}')
            self.last_cmd_time = time.time()
            console.print(f"-{self.user}[+] ran lottery.".center(console_width - 2 ), style = "cyan on black")
            await asyncio.sleep(self.total_seconds + random.uniform(34.377337,93.7473737))
     # Lvl grind
    @tasks.loop()
    async def lvlGrind(self):
        await self.cm.send(generate_random_string()) # Better than sending quotes(In my opinion).
        await asyncio.sleep(random.uniform(lvlGrindCooldown + 0.1, lvlGrindCooldown + 0.4))

#----------ON READY----------#
    async def on_ready(self):
        printBox(f'-Made by EchoQuill'.center(console_width - 2 ),'bold green on black' )
        printBox(f'-version:- 0.0.1'.center(console_width - 2 ),'bold cyan on black' )
        self.on_ready_dn = False
        self.cmds = 1
        self.cmds_cooldown = 0
        await asyncio.sleep(1)
        printBox(f'-Loaded {self.user.name}[*].'.center(console_width - 2 ),'bold purple on black' )
        listUserIds.append(self.user.id)
        await asyncio.sleep(0.12)
        self.cm = self.get_channel(self.channel_id)
        qtemp.append(self.cm.guild.id)
        self.dm = await self.fetch_user(408785106942164992)
        self.list_channel.append(self.dm.dm_channel.id)
        self.qtemp = False
        self.qtemp2 = True
        self.owoQuest = False
        self.friendCurseQuest = False
        self.friendPrayQuest = False
        self.cookieQuest = False
        self.actionQuest = False
        self.owoTempInt = 0
        self.owoTempIntTwo = 0
        self.battleWithFriendQuest = False
        self.hunt = None
        self.battle = None
        self.justStarted = True
        self.list_channel = [self.channel_id, self.dm.dm_channel.id]
        try:
            self.owoSupportChannel = self.get_channel(465978474163601436)
            self.list_channel.append(self.owoSupportChannel.channel.id)
        except:
            self.owoSupportChannel = None
        self.spams = 0
        self.last_cmd_time = 0
        self.lastcmd = None
        self.busy = False
        self.hb = 0
        self.ss = 0
        self.hCount = 0
        self.time_since_last_cmd = 0
        self.tempForCheck = False
        self.f = False
        self.questDone = False
        self.gemHuntCnt = None
        self.gemEmpCnt = None
        self.gemLuckCnt = None
        self.gemSpecialCnt = None
        # Starting hunt/battle loop
        if autoHunt or autoBattle:
            if autoHunt and autoBattle:
                self.huntOrBattle = None
                self.huntOrBattleSelected = False
            elif autoHunt:
                self.huntOrBattle = "hunt"
                self.huntOrBattleSelected = True
            else:
                self.huntOrBattle = "battle"
                self.huntOrBattleSelected = True
            self.send_hunt_or_battle.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
         # Starting curse/pray loop
        if autoCurse or autoPray:
            if autoCurse:
                self.prayOrCurse = "curse"
            else:
                self.prayOrCurse = "pray"
            self.send_curse_and_prayer.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        # Starting Daily loop
        if autoDaily:
            self.send_daily.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        # Starting Auto Owo
        if autoOwo:
            self.send_owo.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        # Starting Coinflip
        if autoCf:
            self.cfAmt = cfAmt
            self.cfCooldown = cfCooldown
            self.cfAllotedValue = cfAllotedValue
            self.cft = cfAllotedValue
            self.cfN = 1
            self.cfu = cfAmt
            self.cfDoubleOnLose = config["commands"][6]["doubleOnLose"]
            self.send_cf.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        # Starting slots CHEXK
        if autoCf:
            self.slotsAmt = slotdAmt
            self.slotsAllotedValue = cfAllotedValue
            self.cft = cfAllotedValue
            self.cfN = 1
            self.cfu = cfAmt
            self.cfDoubleOnLose = config["commands"][6]["doubleOnLose"]
            self.send_cf.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        # Start Sell or Sac
        if autoSell or autoSac:
            if autoSell and autoSac:
                self.huntOrBattle = None
                self.sellOrSacSelected = False
            elif autoSell:
                self.huntOrBattle = "sell"
                self.sellOrSacSelected = True
            else:
                self.huntOrBattle = "sac"
                self.sellOrSacSelected = True
            self.send_sell_or_sac.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        if customCommands:
            self.send_custom.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        if autoQuest:
            self.check_quests.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        if lottery:
            self.send_lottery.start()

        embed1 = discord.Embed(
            title='logging in',
            description=f'logged in as {self.user.name}',
            color=discord.Color.dark_green()
        )

        if webhookEnabled:
            self.webhook = SyncWebhook.from_url(webhook_url)
            self.webhook.send(embed=embed1, username='uwu bot') 
        await asyncio.sleep(random.uniform(2.69,3.69))
        if desktopNotificationEnabled:
            pass
        self.justStarted = False
        printBox(f'-Loaded all accounts.'.center(console_width - 2 ),'bold magenta on black' )
        print('-'*console_width)
#----------ON MESSAGE----------#
    async def on_message(self, message):
        if not self.is_ready():
            return
        if message.author.id != 408785106942164992:
            return
        if any(b in message.content.lower() for b in list_captcha) and message.channel.id in self.list_channel:
            self.f = True
            if termuxNotificationEnabled:
                os.system("termux-notification -c 'captcha detected!'")
                os.system(f"termux-toast -c red -b black 'Captcha Detected:- {self.user.name}")
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
            pass
        if message.channel.id == self.channel_id and "slow down and try the command again" in message.content.lower():
            await asyncio.sleep(random.uniform(3.9,5.2))
            if self.lastcmd == "hunt":
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}h")
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.lastcmd == "battle":
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}b")
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
        if message.channel.id == self.channel_id and ('you found' in message.content.lower() or "caught" in message.content.lower()):
            self.hb = 1
            self.last_cmd_time = time.time()
            self.lastcmd = "hunt"
            if "you found" in message.content.lower():
                self.sendingGemsIds = ""
                if autoHuntGem:
                    for i in huntGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                self.tempForCheck = False
                if autoEmpoweredGem:
                    for i in empGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                self.tempForCheck = False
                if autoLuckyGem:
                    for i in luckyGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                self.tempForCheck = False
                if autoSpecialGem:
                    for i in specialGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                self.tempForCheck = False
                await self.cm.send(f'{setprefix}use {self.sendingGemsIds}')
                console.print(f"-{self.user}[+] used gems({self.sendingGemsIds})".center(console_width - 2 ), style = "Cyan on black")
        if message.channel.id == self.channel_id and ("you found a **lootbox**!" in message.content.lower() or "you found a **weapon crate**!" in message.content.lower()):
            if "**lootbox**" in message.content.lower() and autoLootbox:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}lb all")
                console.print(f"-{self.user}[+] used lootbox".center(console_width - 2 ), style = "magenta on black")
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                
            elif "**weapon crate**" in message.content.lower() and autoCrate:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}crate all")
                console.print(f"-{self.user}[+] used all crates".center(console_width - 2 ), style = "magenta on black")
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
        if "inventory" in message.content.lower() and "=" in message.content.lower():
            self.invNumbers = re.findall(r'`(\d+)`', text)         
        if message.embeds and message.channel.id == self.channel_id:
            for embed in message.embeds:
                if embed.author.name is not None and "goes into battle!" in embed.author.name.lower():
                    self.hb = 0 #check
                    self.last_cmd_time = time.time()
                    self.lastcmd = "battle"
                if embed.author.name is not None and "quest log" in embed.author.name.lower():
                    if "you finished all of your quests!" in embed.description.lower():
                        self.qtemp = True
                        return
                    if "Say 'owo'" not in message.content:
                        self.owoQuest = False
                    else:
                        self.owoTempIntTwo = re.findall(r"\'owo\'\s*(\d+)\s*times", message.content)
                        if autoOwo == False:
                            self.send_owo.start()
                        self.owoQuest = True
                    if "Have a friend pray to you" not in message.content:
                        self.friendPrayQuest = False
                    else:
                        #self.prayTempIntTwo = re.findall(r"\'owo\'\s*(\d+)\s*times", message.content)
                        if self.owoSupportChannel != None and self.qtemp2 == False:
                            await self.owoSupportChannel.send("owo quest")
                            self.qtemp2 = True
                        self.friendPrayQuest = True
                    if "Have a friend curse you" not in message.content:
                        self.friendCurseQuest = False
                    else:
                        #self.curseTempIntTwo = re.findall(r"\'owo\'\s*(\d+)\s*times", message.content)
                        if self.owoSupportChannel != None and self.qtemp2 == False:
                            await self.owoSupportChannel.send("owo quest")
                            self.qtemp2 = True
                        self.friendCurseQuest = True
                    if "Receive a cookie from 1 friends" not in message.content:
                        self.cookieQuest = False
                    else:
                        #self.cookieTempIntTwo = re.findall(r"\'owo\'\s*(\d+)\s*times", message.content)
                        if self.owoSupportChannel != None and self.qtemp2 == False:
                            await self.owoSupportChannel.send("owo quest")
                            self.qtemp2 = True
                        self.cookieQuest = True
                        if "xp from hunting and battling" not in message.content:
                            pass
                        else:
                            pass
                        if "Use an action" not in message.content:
                            self.actionQuest = False
                        else:
                            if self.owoSupportChannel != None and self.qtemp2 == False:
                                await self.owoSupportChannel.send("owo quest")
                                self.qtemp2 = True
                            self.actionQuest = True
                        if "Battle with a friend" not in message.content:
                            pass
                        else:
                            if self.owoSupportChannel != None and self.qtemp2 == False:
                                await self.owoSupportChannel.send("owo quest")
                                self.qtemp2 = True
             
#----------ON MESSAGE EDIT----------#
    async def on_message_edit(self, before, after):
        #print("ed")
        if before.author.id != 408785106942164992:
            return
        if before.channel.id != self.channel_id:
            return
        # slots
        if "slots" in after.content.lower():
            if "won" in after.content.lower() and ":c" in after.content.lower():
                self.slotsFail = True
                self.slotsT-=self.slotsAmt*self.slotsN
                if self.slotsDoubleOnLose:
                    self.slotsN = 1
            else:
                print("won")
                if "<:eggplant:417475705719226369>" in after.content.lower():
                    self.slotsNope = True
                else:
                    self.match = re.search(r'won <:cowoncy:416043450337853441> (\d{1,3}(?:,\d{3})*(?:\.\d+)?)', after.content)
                    self.slotsT+=int(match.group(1).replace(',', ''))
                    if self.slotsDoubleOnLose:
                        self.slotsN += 1
                    self.slotsWon = True
        #coinflip
        if "chose" in after.content.lower():
            if "and you lost it all... :c" in after.content.lower():
                self.match = re.search(r'<:cowoncy:416043450337853441> (\d{1,3}(?:,\d{3})*)(?:\.\d+)?', after.content)
                self.cft-=int(self.match.group(1).replace(',', ''))
                console.print(f"-{self.user}[+] ran Coinflip and lost {self.match.group(1).replace(',', '')} cowoncy!.".center(console_width - 2 ), style = "magenta on black")
                if self.cfDoubleOnLose:
                    self.cfN += 1
            else:
                self.match = re.search(r'won \*\*<:cowoncy:416043450337853441> (\d{1,3}(?:,\d{3})*(?:\.\d+)?)', after.content)
                console.print(f"-{self.user}[+] ran Coinflip and won {self.match.group(1).replace(',', '')} cowoncy!.".center(console_width - 2 ), style = "magenta on black")
                self.cft+=int(self.match.group(1).replace(',', ''))
                if self.cfDoubleOnLose:
                    self.cfN = 1
                
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
    client = MyClient(token, channel_id)
    client.run(token, log_handler=None)
if __name__ == "__main__":
    console.print(owoPanel)
    print('-'*console_width)
    if autoPray == True and autoCurse == True:
        console.print("Both autoPray and autoCurse enabled", style = "red on black")
    if termuxNotificationEnabled and desktopNotificationEnabled:
        console.print("Only enable either termux notifs of desktop notifs.", style = "red on black")
    
    tokens_and_channels = [line.strip().split() for line in open("toke.txt", "r")]
    run_bots(tokens_and_channels)
