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
import threading
import requests
import random
import asyncio
import logging
import discord
import secrets
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
list_captcha = ["to check that you are a human!","https://owobot.com/captcha","please reply with the following", "captcha"]
mobileBatteryCheckEnabled = config["termuxAntiCaptchaSupport"]["batteryCheck"]["enabled"]
mobileBatteryStopLimit = config["termuxAntiCaptchaSupport"]["batteryCheck"]["minPercentage"]
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
if autoHuntGem or autoEmpoweredGem or autoLuckyGem or autoSpecialGem:
    autoGem = True
else:
    autoGem = False
autoSell = config["commands"][2]["sell"]
autoSac = config["commands"][2]["sacrifice"]
autoQuest = config["commands"][6]["quest"]
ignoreDisable_Quest = config["commands"][6]["doEvenIfDisabled"]
rarity = ""
for i in config["commands"][2]["rarity"]:
    rarity = rarity + i + " "
autoCf = config["commands"][4]["coinflip"]
autoSlots = config["commands"][3]["slots"]
customCommands = config["customCommands"]["enabled"]
lottery = config["commands"][7]["lottery"]
lotteryAmt = config["commands"][7]["amount"]
lvlGrind = config["commands"][8]["lvlGrind"]
customCommandCnt = -1
for i in config["customCommands"]["commands"]:
    customCommandCnt+=1
if customCommandCnt >= 1:
    sorted_zipped_lists = sorted(zip(config["customCommands"]["commands"], config["customCommands"]["cooldowns"]), key=lambda x: x[1]) 
    sorted_list1, sorted_list2 = zip(*sorted_zipped_lists)
elif customCommandCnt == 0:
    sorted_list1 = config["customCommands"]["commands"]
    sorted_list2 = config["customCommands"]["cooldowns"]
#lotter amt check:-
if lotteryAmt > 250000:
    lotteryAmt = 250000
# Gems.
huntGems = ["057","056","055","054","053","052","051"]
empGems = ["071","070","069","068","067","066","065"]
luckGems = ["078","077","076","075","074","073","072"]
specialGems = ["085","084","083","082","081","080","079"]
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
# For battery check
def batteryCheckFunc():
    while True:
        time.sleep(120)
        battery_status = os.popen("termux-battery-status").read()
        battery_data = json.loads(battery_status)
        percentage = battery_data['percentage']
        console.print(f"-system[0] Current battery •> {percentage}".center(console_width - 2 ), style = "blue on black")
        if percentage < mobileBatteryStopLimit:
            break
    os._exit(0)
if mobileBatteryCheckEnabled:
    loop_thread = threading.Thread(target=batteryCheckFunc)
    loop_thread.start()
#-------------
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
        if self.f != True:
            if self.justStarted:
                await asyncio.sleep(random.uniform(21,67))
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}daily")
                self.last_cmd_time = time.time()
                self.lastcmd = "daily"
                console.print(f"-{self.user}[+] ran daily (next daily :> {self.formatted_time})".center(console_width - 2 ), style = "Cyan on black")
            self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
            self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst
        
            self.formatted_time = "{:02}h {:02}m {:02}s".format(
                int(self.time_until_12am_pst.total_seconds() // 3600),
                int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
                int(self.time_until_12am_pst.total_seconds() % 60)
)
            self.total_seconds = self.time_until_12am_pst.total_seconds()
        #print(f"Time till mext daily for {self.user.name} = {self.formatted_time}")
            await asyncio.sleep(self.total_seconds+random.uniform(30,90))
            self.current_time = time.time()
            self.time_since_last_cmd = self.urrent_time - self.last_cmd_time
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
            await self.cm.send(f"{setprefix}daily")
            console.print(f"-{self.user}[+] ran daily (next daily :> {self.formatted_time})".center(console_width - 2 ), style = "Cyan on black")
            self.lastcmd = "daily"
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    #hunt/battle
    @tasks.loop()
    async def send_hunt_or_battle(self):
        if not self.huntOrBattleSelected:
            if self.hb == 1:
                self.huntOrBattle = "battle"
            elif self.hb == 0:
                self.huntOrBattle = "hunt"
        if self.lastHb == 0:
            await asyncio.sleep(random.uniform(2.5,3.5))
        self.lastHb = self.hb
        if self.f != True:
            self.current_time = time.time()
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
            else:
                pass
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if not self.tempHuntDisable:
                await self.cm.send(f'{setprefix}{self.huntOrBattle}')
                console.print(f"-{self.user}[+] ran {self.huntOrBattle}.".center(console_width - 2 ), style = "purple on black")
                if self.hb == 1:
                    await asyncio.sleep(huntOrBattleCooldown + random.uniform(0.99, 1.10))
                else:
                    await asyncio.sleep(random.uniform(0.3,0.6))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
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
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     #coinflip jejejdjdj
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
            if self.slotsAmt*self.slotsN > 250000:
                console.print(f"-{self.user}[-] Stopping slots [250k exceeded]".center(console_width - 2 ), style = "red on black")
                self.send_slots.stop()
            elif self.slotsAllotedValue < self.slotsT:
                console.print(f"-{self.user}[-] Stopping slots [allotted value exceeded]".center(console_width - 2 ), style = "red on black")
                self.send_slots.stop()
            await self.cm.send(f'{setprefix}slots {slotsAmt*slotsN}')
            console.print(f"-{self.user}[+] ran Coinflip.".center(console_width - 2 ), style = "cyan on black")
            await asyncio.sleep(slotsCooldown + random.uniform(0.28288282, 0.928292929))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
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
            if autoOwo == False and self.owoQuest == True:
                self.owoTempInt+=1 
                if self.owoTempInt == self.owoTempIntTwo:
                    self.send_owo.stop()
            await asyncio.sleep(random.uniform(19.28288282, 21.928292929))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
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
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     # Custom commands
    @tasks.loop()
    async def send_custom(self):
        if self.f != True:
            for i in range(customCommandCnt):
                if i != 0 and i+1 < customCommandCnt:                  
                    await asyncio.sleep(random.uniform((sorted_list2[i] - sorted_list2[i-1]) + 0.3, (sorted_list2[i] - sorted_list2[i-1]) + 0.5))
                elif i == 0:
                    await asyncio.sleep(random.uniform(sorted_list2[i] + 0.3, sorted_list2[i] + 0.5))
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
                await self.cm.send(sorted_list1[i])
                self.last_cmd_time = time.time()
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
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
            self.last_cmd_time = time.time()
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
        else:        
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    # Lottery
    @tasks.loop()
    async def send_lottery(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            await self.cm.send(f'{setprefix}lottery {lotteryAmt}')
            self.last_cmd_time = time.time()
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
            console.print(f"-{self.user}[+] ran lottery. {self.total_seconds}".center(console_width - 2 ), style = "cyan on black")
            await asyncio.sleep(self.total_seconds + random.uniform(34.377337,93.7473737))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     # Lvl grind
    @tasks.loop()
    async def lvlGrind(self):
        if self.f != True:
            await self.cm.send(generate_random_string()) # Better than sending quotes(In my opinion).
            await asyncio.sleep(random.uniform(lvlGrindCooldown + 0.1, lvlGrindCooldown + 0.4))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))

#----------ON READY----------#
    async def on_ready(self):
        self.on_ready_dn = False
        self.cmds = 1
        self.cmds_cooldown = 0
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
        self.tempHuntDisable = False
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
        self.lastHb = None
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
        self.invCheck = False
        # Starting hunt/battle loop
        self.on_ready_dn = True
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
            self.cfAmt = config["commands"][4]["startValue"]
            self.cfAllotedValue = config["commands"][4]["allottedAmount"]
            self.cft = config["commands"][4]["allottedAmount"]
            self.cfN = 1
            self.cfDoubleOnLose = config["commands"][6]["doubleOnLose"]
            self.send_cf.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        # Starting slots CHEXK
        if autoSlots:
            self.slotsAmt = config["commands"][3]["startValue"]
            self.slotsAllotedValue = config["commands"][3]["allottedAmount"]
            self.slotsT = config["commands"][3]["startValue"]
            self.slotsN = 1
            self.cfDoubleOnLose = config["commands"][6]["doubleOnLose"]
            self.send_slots.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        # Start Sell or Sac
        if autoSell or autoSac:
            if autoSell and autoSac:
                self.sellOrSac = None
                self.sellOrSacSelected = False
            elif autoSell:
                self.sellOrSac = "sell"
                self.sellOrSacSelected = True
            else:
                self.sellOrSac = "sac"
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
        if lvlGrind:
            self.lvlGrind.start()
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
#----------ON MESSAGE----------#
    async def on_message(self, message):
        if not self.on_ready_dn:
            return
        if message.author.id != 408785106942164992:
            return
        if any(b in message.content.lower() for b in list_captcha) and message.channel.id in self.list_channel:
            if "**👍 |** I have verified that you are human! Thank you! :3" in message.content and message.channel.id in self.list_channel:
                self.f = False
                console.print(f"-{self.user}[+] Captcha solved. restarting...".center(console_width - 2 ), style = "dark_magenta on black")
                return
            self.f = True
            if termuxNotificationEnabled:
                os.system(f"termux-notification -c 'captcha detected! {self.user.name}'")
                os.system(f"termux-toast -c red -b black 'Captcha Detected:- {self.user.name}'")
            console.print(f"-{self.user}[!] CAPTCHA DETECTED. waiting...".center(console_width - 2 ), style = "deep_pink2 on black")
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
        if "**👍 |** I have verified that you are human! Thank you! :3" in message.content and message.channel.id in self.list_channel:
            self.f = False
            console.print(f"-{self.user}[+] Captcha solved. restarting...".center(console_width - 2 ), style = "dark_magenta on black")
        if message.channel.id == self.channel_id and "please slow down~ you're a little **too fast** for me :c" in message.content.lower():
            pass
        if message.channel.id == self.channel_id and "slow down and try the command again" in message.content.lower():
            await asyncio.sleep(random.uniform(3.9,5.2))
            if self.lastcmd == "hunt":
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}hunt")
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.lastcmd == "battle":
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}battle")
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
        if message.channel.id == self.channel_id and ('you found' in message.content.lower() or "caught" in message.content.lower()):
            self.hb = 1
            self.last_cmd_time = time.time()
            self.lastcmd = "hunt"
            if "caught" in message.content.lower() and autoGem:
                self.current_time = time.time()
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}inventory")
                console.print(f"-{self.user}[~] checking Inventory....".center(console_width - 2 ), style = "Cyan on black")
                self.invCheck = True
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
        if message.channel.id == self.channel_id and "Inventory" in message.content and "=" in message.content.lower():
            if self.invCheck:
                self.invNumbers = re.findall(r'`(\d+)`', message.content)
                self.tempHuntDisable = True
                self.tempForCheck = False
                self.sendingGemsIds = ""
                if autoHuntGem:
                    for i in huntGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds = self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break                            
                self.tempForCheck = False
                if autoEmpoweredGem:
                    for i in empGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds = self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                self.tempForCheck = False
                if autoLuckyGem:
                    for i in luckGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds = self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                self.tempForCheck = False
                if autoSpecialGem:
                    for i in specialGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds = self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                self.tempForCheck = False
               # print(self.sendingGemsIds)
                if self.sendingGemsIds != "":
                    await self.cm.send(f'{setprefix}use {self.sendingGemsIds}')
                    console.print(f"-{self.user}[+] used gems({self.sendingGemsIds})".center(console_width - 2 ), style = "Cyan on black")
                    self.last_cmd_time = time.time()
                self.invCheck = False
                self.tempHuntDisable = False
                self.sendingGemsIds = ""
        if message.embeds and message.channel.id == self.channel_id:
            for embed in message.embeds:
                if embed.author.name is not None and "goes into battle!" in embed.author.name.lower():
                    self.hb = 0 #check
                    self.last_cmd_time = time.time()
                    self.lastcmd = "battle"
                if embed.author.name is not None and "quest log" in embed.author.name.lower():
                    if not autoQuest:
                        return
                    if "you finished all of your quests!" in embed.description.lower():
                        self.qtemp = True
                        self.qtemp2 = False
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
    printBox(f'-Made by EchoQuill'.center(console_width - 2 ),'bold green on black' )
    printBox(f'-version:- 0.0.8'.center(console_width - 2 ),'bold cyan on black' )
    if autoPray == True and autoCurse == True:
        console.print("Both autoPray and autoCurse enabled", style = "red on black")
    if termuxNotificationEnabled and desktopNotificationEnabled:
        console.print("Only enable either termux notifs of desktop notifs.", style = "red on black")
    tokens_and_channels = [line.strip().split() for line in open("toke.txt", "r")]
    token_len = len(tokens_and_channels)
    printBox(f'-Loaded {token_len} accounts.'.center(console_width - 2 ),'bold magenta on black' )
    #print(token_len)
    run_bots(tokens_and_channels)