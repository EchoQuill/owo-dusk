# Iam obsessed with imports being in descending order.
# Written by EchoQuill, on a laggy mobile.
# Make sure to star the github page.

from flask import Flask, request, render_template, jsonify, redirect, url_for
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord import SyncWebhook
from rich.console import Console
from threading import Thread
from rich.panel import Panel
import discord.errors
import subprocess
import threading
import requests
import random
import asyncio
import logging
import discord
import aiohttp
import secrets
import ctypes
import string
import shutil
import time
import json
import sys
import os
import re
# Set AppUserModleId thingy
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("OwO-Dusk")
except AttributeError:
    pass
def clear():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Others
        os.system('clear')
clear()
# For console.log thingy
console = Console()
# Random module seed for better anti detection.
#seed = secrets.randbelow(4765839360747)
#random.seed(seed)
# Console width size
console_width = shutil.get_terminal_size().columns
# Owo text art for panel 
owoArt = """
  __   _  _   __       ____  _  _  ____  __ _ 
 /  \ / )( \ /  \  ___(    \/ )( \/ ___)(  / )
(  O )\ /\ /(  O )(___)) D () \/ (\___ \ )  ( 
 \__/ (_/\_) \__/     (____/\____/(____/(__\_)
"""
# Num:- 5, Font:- Gracefull.
owoPanel = Panel(owoArt, style="purple on black", highlight=False)

# Load json file
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
with open(resource_path("config.json")) as file:
    config = json.load(file)
#----------OTHER VARIABLES----------#
version = "1.2.2"
offline = config["offlineStatus"]
ver_check_url = "https://raw.githubusercontent.com/EchoQuill/owo-dusk/main/version.txt"
quotesUrl = "https://thesimpsonsquoteapi.glitch.me/quotes"
ver_check = requests.get(ver_check_url).text.strip()
typingIndicator = config["typingIndicator"]
list_captcha = ["to check that you are a human!","https://owobot.com/captcha","please reply with the following", "captcha"]
mobileBatteryCheckEnabled = config["termux"]["batteryCheck"]["enabled"]
mobileBatteryStopLimit = config["termux"]["batteryCheck"]["minPercentage"]
batteryCheckSleepTime = config["termux"]["batteryCheck"]["refreshInterval"]
termuxNotificationEnabled = config["termux"]["notifications"]["enabled"]
notificationCaptchaContent = config["termux"]["notifications"]["captchaContent"]
notificationBannedContent = config["termux"]["notifications"]["bannedContent"]
termuxToastEnabled = config["termux"]["toastOnCaptcha"]["enabled"]
toastBgColor = config["termux"]["toastOnCaptcha"]["backgroundColour"]
toastTextColor = config["termux"]["toastOnCaptcha"]["textColour"]
toastCaptchaContent = config["termux"]["toastOnCaptcha"]["captchaContent"]
toastBannedContent = config["termux"]["toastOnCaptcha"]["bannedContent"]
termuxTtsEnabled = config["termux"]["texttospeech"]["enabled"]
termuxTtsContent = config["termux"]["texttospeech"]["content"]
termuxAudioPlayer = config["termux"]["playAudio"]["enabled"]
termuxAudioPlayerPath = config["termux"]["playAudio"]["path"]
termuxVibrationEnabled = config["termux"]["vibrate"]["enabled"]
termuxVibrationTime = config["termux"]["vibrate"]["time"] * 1000
desktopNotificationEnabled = config["desktop"]["notifications"]["enabled"]
desktopNotificationCaptchaContent = config["desktop"]["notifications"]["captchaContent"]
desktopNotificationBannedContent = config["desktop"]["notifications"]["bannedContent"]
desktopAudioPlayer = config["desktop"]["playAudio"]["enabled"]
desktopAudioPlayerPath = config["desktop"]["playAudio"]["path"]
websiteEnabled = config["website"]["enabled"]
websitePort = config["website"]["port"]
captchaConsoleEnabled = config["console"]["runConsoleCommandOnCaptcha"]
banConsoleEnabled = config["console"]["runConsoleCommandOnBan"]
if captchaConsoleEnabled:
    captchaConsoleContent = config["console"]["commandToRunOnCaptcha"]
if banConsoleEnabled:
    banConsoleContent = config["console"]["commandToRunOnBan"]

# ___Dble check these___
def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def try_import_or_install(package_name):
    try:
        __import__(package_name)
        print(f"Module {package_name} imported successfully.")
    except ImportError:
        print(f"-System[0] {package_name} is not installed, attempting to install automatically...")
        try:
            install_package(package_name)
            __import__(package_name)
            print(f"{package_name} installed and imported successfully.")
        except Exception as e:
            print(f"Failed to install {package_name}. Please run 'pip install {package_name}' and run the script again. Error: {e}")
if desktopNotificationEnabled:
    try_import_or_install("plyer")
    # Import notification from plyer
    try:
        from plyer import notification
        print("Notification module in plyer imported successfully.")
    except ImportError as e:
        print(f"ImportError: {e}")
        
if desktopAudioPlayer:
    try_import_or_install("playsound3")
    # Import playsound from playsound3
    try:
        from playsound3 import playsound
        print("Playsound module in playsound3 imported successfully.")
    except ImportError as e:
        print(f"ImportError: {e}")
        
#_________
        
#if termuxTtsEnabled:
#    clear()
#    os.system("mkfifo ~/.tts")
 #   console.print(f"-System[0] setting up Text To Speech for faster usage... if this takes way too long then you should consider disabling Termux TTs...", style = "cyan on black")
#    os.system("cat ~/.tts | termux-tts-speak")
#    clear()
webhookEnabled = config["webhook"]["enabled"]
if webhookEnabled:
    webhook_url = config["webhook"]["webhookUrl"]
    webhookUselessLog = config["webhook"]["webhookUselessLog"]
    dwebhook = SyncWebhook.from_url(webhook_url)
    webhookPingId = config["webhook"]["webhookUserIdToPingOnCaptcha"]
    webhookCaptchaChnl = config["webhook"]["webhookCaptchaUrl"]
else:
    webhookUselessLog = False
setprefix = config["setprefix"]
#----------MAIN VARIABLES----------#
listUserIds = []
autoHunt = config["commands"][0]["hunt"]
autoBattle = config["commands"][0]["battle"]
useShortForm = config["commands"][0]["useShortForm"]
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
autoQuest = config["commands"][4]["quest"]
askForHelpChannel = config["commands"][4]["askForHelpChannel"]
askForHelp = config["commands"][4]["askForHelp"]
doEvenIfDisabled = config["commands"][4]["doEvenIfDisabled"]
rarity = ""
for i in config["commands"][2]["rarity"]:
    rarity = rarity + i + " "
autoCf = config["commands"][3]["coinflip"]
cfOptions = config["commands"][3]["cfOptions"]
autoSlots = config["commands"][3]["slots"]
#GAMBLE
doubleOnLose = config["commands"][3]["doubleOnLose"]
gambleAllottedAmount = config["commands"][3]["allottedAmount"]
gambleStartValue = config["commands"][3]["startValue"]
#%%%%%%%
customCommands = config["customCommands"]["enabled"]
lottery = config["commands"][5]["lottery"]
lotteryAmt = config["commands"][5]["amount"]
lvlGrind = config["commands"][6]["lvlGrind"]
useQuoteInstead = config["commands"][6]["useQuoteInstead"]
lvlMinLength = config["commands"][6]["minLengthForRandomString"]
lvlMaxLength = config["commands"][6]["maxLengthForRandomString"]
cookie = config["commands"][7]["cookie"]
cookieUserId = config["commands"][7]["userid"]
sleepEnabled = config["commands"][8]["sleep"]
minSleepTime = config["commands"][8]["minTime"]
maxSleepTime = config["commands"][8]["maxTime"]
sleepRandomness = config["commands"][8]["randomness"]
giveawayEnabled = config["commands"][9]["giveawayJoiner"]
giveawayChannels = config["commands"][9]["channelsToJoin"]
shopEnabled = config["commands"][10]["shop"]
shopItemsToBuy = config["commands"][10]["itemsToBuy"]
customCommandCnt = len(config["customCommands"]["commands"])
if customCommandCnt >= 1:
    sorted_zipped_lists = sorted(zip(config["customCommands"]["commands"], config["customCommands"]["cooldowns"]), key=lambda x: x[1])
    sorted_list1, sorted_list2 = zip(*sorted_zipped_lists)
else:
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
if config["autoUse"]["autoGem"]["order"]["lowestToHighest"]:
    huntGems.reverse()
    empGems.reverse()
    luckGems.reverse()
    specialGems.reverse()
questsList = []

# Cooldowns
huntOrBattleCooldown = [config["commands"][0]["minCooldown"], config["commands"][0]["maxCooldown"]]
prayOrCurseCooldown = [config["commands"][1]["minCooldown"], config["commands"][1]["maxCooldown"]]
sellOrSacCooldown = [config["commands"][2]["minCooldown"], config["commands"][2]["maxCooldown"]]
gambleCd = [config["commands"][3]["minCooldown"], config["commands"][3]["maxCooldown"]]
lvlGrindCooldown = [config["commands"][6]["minCooldown"], config["commands"][6]["maxCooldown"]]
shopCd = [config["commands"][10]["minCooldown"], config["commands"][10]["maxCooldown"]]
gawMaxCd = config["commands"][9]["maxCooldown"]
gawMinCd = config["commands"][9]["minCooldown"]
# Box print
def printBox(text, color):
    test_panel = Panel(text, style=color)
    console.print(test_panel)
# For lvl grind
def generate_random_string():
    characters = string.ascii_lowercase + ' '
    length = random.randint(lvlMinLength, lvlMaxLength)
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string
# For battery check
def batteryCheckFunc():
    try:
        while True:
            time.sleep(batteryCheckSleepTime)
            try:
                battery_status = os.popen("termux-battery-status").read()
            except Exception as e:
                console.print(f"""-system[0] Battery check failed!!
Keep in mind that Battery check is only available for Termux users.
also termux is also only for android/termux users. disable those if your not on Termux/Android...
try using desktopNotificationEnabled instead if your not on termux.""".center(console_width - 2 ), style = "red on black")
            battery_data = json.loads(battery_status)
            percentage = battery_data['percentage']
            console.print(f"-system[0] Current battery •> {percentage}".center(console_width - 2 ), style = "blue on black")
            if percentage < mobileBatteryStopLimit:
                break
    except Exception as e:
        print("battery check", e)
    os._exit(0)
if mobileBatteryCheckEnabled:
    loop_thread = threading.Thread(target=batteryCheckFunc)
    loop_thread.start()
#For emoji names
try:
    with open("emojis.json", 'r', encoding="utf-8") as file:
        emoji_dict = json.load(file)
except FileNotFoundError:
    print("The file emojis.json was not found.")
except json.JSONDecodeError:
    print("Failed to decode JSON from the file.")
def get_emoji_names(text, emoji_dict=emoji_dict):
    # Extract all emojis and custom emoji strings from the text
    pattern = re.compile(r"<a:[a-zA-Z0-9_]+:[0-9]+>|[\U0001F300-\U0001F6FF\U0001F700-\U0001F77F]")
    emojis = pattern.findall(text)
    # Get names of the extracted emojis
    emoji_names = [emoji_dict[char] for char in emojis if char in emoji_dict]
    return emoji_names
# Webhook Logging
def webhookSender(msg, desc=None, channel_id=None, plain_text_msg=None):
    try:
        emb = discord.Embed(
            title=msg,
            description=desc,
            color=discord.Color.purple()  # Double check
        )

        if channel_id:
            # Create a new webhook instance for the specific channel ID
            channel_webhook_url = f"https://discord.com/api/webhooks/{channel_id}/{webhook_url.split('/')[-1]}"
            channel_webhook = SyncWebhook.from_url(channel_webhook_url)
            # Send both the embed and plain text message if provided
            if plain_text_msg:
                channel_webhook.send(content=plain_text_msg, embed=emb, username='uwu bot warnings')
            else:
                channel_webhook.send(embed=emb, username='uwu bot warnings')
        else:
            # Send both the embed and plain text message if provided
            if plain_text_msg:
                dwebhook.send(content=plain_text_msg, embed=emb, username='uwu bot warnings')
            else:
                dwebhook.send(embed=emb, username='uwu bot warnings')
    except discord.Forbidden as e:
        print("Bot does not have permission to execute this command:", e)
    except discord.NotFound as e:
        print("The specified command was not found:", e)
    except Exception as e:
        print(e)

 # Count the number of '\n' characters in the text
def count_line_breaks(text):
    line_breaks = text.count('\n')
    return line_breaks
   
# Get dm or channel name
def get_channel_name(channel):
    if isinstance(channel, discord.DMChannel):
        return "owo DMs"
    return channel.name
    
# CAPTCHA NOTIFIER {TERMUX}

def run_system_command(command, timeout, retry=False, delay=5):
    def target():
        try:
            os.system(command)
        except Exception as e:
            print(f"Error executing command: {command} - {e}")

    # Create and start a thread to execute the command
    thread = threading.Thread(target=target)
    thread.start()
    
    # Wait for the thread to finish, with a timeout
    thread.join(timeout)
    
    # If the thread is still alive after the timeout, terminate it
    if thread.is_alive():
        console.print(f"-error[0] {command} command failed!".center(console_width - 2 ), style = "red on black")
        if retry:
            console.print(f"-system[0] Retrying '{command}' after {delay}s".center(console_width - 2 ), style = "blue on black")
            time.sleep(delay)
            run_system_command(command, timeout, retry=False)
        
#-------------


#----------------------
#WEBSITE
#_____________


#APP
app = Flask(__name__)

# List to store captcha data
captchas = []
captchaAnswers = []
# API endpoint to add captchas
@app.route('/add_captcha', methods=['POST'])
def add_captcha():
    # Get data from API request
    data = request.get_json()
    captcha_type = data.get('type')
    url = data.get('url')
    username = data.get('username')

    # Add captcha to the list
    temp_index = len(captchas)
    captchaAnswers.append(None)
    captchas.append({'type': captcha_type, 'url': url, 'username': username})
    print(captchas)
    print(captchaAnswers)    
    # Return a response
    return jsonify({'status': temp_index})

# Render the main page
@app.route('/', methods=['GET'])
def index():
    try:
        if not captchas:
            # Render the green text if there are no captchas
            return render_template('index.html', no_captchas=True)
        else:
            # Render the page with captcha boxes
            return render_template('index.html', captchas=captchas)
    except Exception as e:
        print(f"error in index(): <index.html> :-> {e}")

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get the text from the input bar
    captcha_ans = request.form.get('text')
    captcha_index = request.form.get('captcha_index', type=int) 
    captchaAnswers[captcha_index] = captcha_ans
    print(captcha_ans)
    print(captchaAnswers[captcha_index])
    # Redirect back to the index page
    return redirect(url_for('index'))

def web_start():
    flaskLog = logging.getLogger('werkzeug')
    flaskLog.disabled = True
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    try:
        app.run(debug=False, use_reloader=False, port=websitePort)
    except Exception as e:
        print(e)
if websiteEnabled:
    try:
        web_thread = threading.Thread(target=web_start)
        web_thread.start()
    except Exception as e:
        print(e)

#-------------
class MyClient(discord.Client):
    def __init__(self, token, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = int(channel_id)
        self.list_channel = [self.channel_id]
    #send messages
    async def sendCommands(self, channel, message, typing=False):
        try:
        # await sendCommands(channel=channel, message="", typing=typingIndicator)
            if typing:
                async with channel.typing():
                    if self.f != True:
                        await channel.send(message)
            elif self.f != True:
                await channel.send(message)
        except Exception as e:
            print("typing", e)
            print(channel, message, typing)
            print(f"are you sure your using correct channel id for {self.user}?")
#----------SENDING COMMANDS----------#
    #custom commands func
    async def send_command_custom(self, command, cooldown):
        try:
            while not self.f and not self.sleep:
                self.current_time = time.time()
                await asyncio.sleep(random.uniform(0.2, 0.5) + cooldown)
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.f != True and self.sleep != True:
                    await self.cm.send(command)
                self.last_cmd_time = time.time()
                print(self.user, command)
        except Exception as e:
            print("send_command error", e)
    #Solve Captchas
    @tasks.loop()
    async def captchaSolver(self):
        if self.webInt != None and self.webSend == True and self.tempJsonData != None:
            self.tempListCount = 0
            #self.captchaAnswerGot = False
            for i in captchas:
                if i == self.tempJsonData:
                    if captchaAnswers[self.tempListCount] != None:
                        console.print(f"-{self.user}[0] Attempting to solve image captcha with {captchaAnswers[self.tempListCount]}".center(console_width - 2 ), style = "blue on black")
                        await self.sendCommands(channel=self.dm, message=captchaAnswers[self.tempListCount], typing=typingIndicator)
                        await asyncio.sleep(random.uniform(5.5,9.7))
                        captchaAnswers[self.tempListCount] = None #To prevent spamming wrong ans.
                self.tempListCount+=1    
            await asyncio.sleep(random.uniform(1.5,2.7))
    # OwO delay check
    @tasks.loop()
    async def delayCheck(self):
        self.lastMsg = None
        async for message in self.cm.history(limit=10):
            if message.author.id == 408785106942164992:
                self.lastMsg = 408785106942164992
                break
        if self.lastMsg is None:
            self.sleep = True
            self.sleepTime = random.uniform(48.8372728, 447.8382828)
            console.print(f"-{self.user}[~] sleeping for {self.sleepTime} seconds ‐ No Msg from owo last 10 msgs.".center(console_width - 2 ), style = "plum4 on black")
            await asyncio.sleep(self.sleepTime)
            console.print(f"-{self.user}[~] Finished sleeping {self.sleepTime} seconds".center(console_width - 2 ), style = "plum4 on black")
            self.sleep = False
            await asyncio.sleep(random.uniform(40,70)) # Give enough time for next messages to be send by selfbot
        await asyncio.sleep(random.uniform(50,100))
    #Sleep
    @tasks.loop()
    async def random_account_sleeper(self):
        if self.f != True and self.sleep != True:
            self.randSleepInt = random.randint(1,100)
            if self.randSleepInt > (100 - sleepRandomness):
                self.sleep = True
                self.sleepTime = random.uniform(minSleepTime, maxSleepTime)
                console.print(f"-{self.user}[~] sleeping for {self.sleepTime} seconds".center(console_width - 2 ), style = "plum4 on black")
                await asyncio.sleep(self.sleepTime)
                console.print(f"-{self.user}[~] Finished sleeping {self.sleepTime} seconds".center(console_width - 2 ), style = "plum4 on black")
                self.sleep = False
            else:
                console.print(f"-{self.user}[~] skipped sleep".center(console_width - 2 ), style = "plum4 on black")
                await asyncio.sleep(random.uniform(60,120))
        else:
            await asyncio.sleep(random.uniform(20,40))
    #daily
    @tasks.loop()
    async def send_daily(self):
        if self.f != True and self.sleep != True:
            await asyncio.sleep(random.uniform(21,67))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
            #await self.cm.send(f"{setprefix}daily")
            await self.sendCommands(channel=self.cm, message=f"{setprefix}daily", typing=typingIndicator)
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
            console.print(f"-{self.user}[+] ran daily (next daily :> {self.formatted_time})".center(console_width - 2 ), style = "Cyan on black")
            if webhookUselessLog:
                webhookSender(f"-{self.user}[+] ran daily", f"next daily in {self.formatted_time}")
            self.lastcmd = "daily"
            await asyncio.sleep(self.total_seconds+random.uniform(30,90))            
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
            else:
                self.hb = 0
                self.huntOrBattle = "hunt"
        #print(self.hb, self.huntOrBattle, self.user, "1")
        if self.f != True and self.sleep != True:
            try:
                self.current_time = time.time()
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                else:
                    pass
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if not self.tempHuntDisable:
                    if self.hb == 0:
                        if self.broke[1]:
                            self.hb = 1
                            self.huntOrBattle = "battle"
                            await asyncio.sleep(random.uniform(huntOrBattleCooldown[0], huntOrBattleCooldown[1]))
                        elif self.lastHb == self.hb == 0 and self.broke[0]:
                            self.broke[1] = True
                            self.broke[0] = False
                        else:
                            #self.broke[False,False]
                            await asyncio.sleep(random.uniform(1.9,3.7))
                    if useShortForm:
                        await self.sendCommands(channel=self.cm, message=f"{setprefix}{self.huntOrBattle[0]}", typing=typingIndicator)
                        #await self.cm.send(f'{setprefix}{self.huntOrBattle[0]}')
                    else:
                        await self.sendCommands(channel=self.cm, message=f"{setprefix}{self.huntOrBattle}", typing=typingIndicator)
                    self.lastHb = self.hb
                    console.print(f"-{self.user}[+] ran {self.huntOrBattle}.".center(console_width - 2 ), style = "purple on black")
                    if webhookUselessLog:
                        webhookSender(f"-{self.user}[+] ran {self.huntOrBattle}.")
                    if (autoBattle == False or autoHunt == False) and (self.huntQuestValue != None or self.battleQuestValue != None):
                        if autoHunt == False and autoBattle == False:
                            self.tempBattleQuestValue+=1
                            self.tempHuntQuestValue+=1
                            if (self.huntQuestValue <= self.tempHuntQuestValue) and (self.battleQuestValue <= self.tempBattleQuestValue):
                                self.battleQuestValue = None
                                self.tempBattleQuestValue = None
                                self.send_hunt_or_battle.stop()
                            elif self.huntQuestValue <= self.tempHuntQuestValue:
                                self.huntOrBattleSelected = False
                                self.huntOrBattle = "battle"
                                self.hb = 1
                                self.battleQuestValue = None
                                self.tempBattleQuestValue = None
                            elif self.battleQuestValue <= self.tempBattleQuestValue:
                                self.huntOrBattleSelected = False
                                self.huntOrBattle = "hunt"
                                self.hb = 0
                                self.battleQuestValue = None
                                self.tempBattleQuestValue = None
                        elif autoHunt:
                            self.tempBattleQuestValue+=1
                            if self.battleQuestValue <= self.tempBattleQuestValue:
                                self.huntOrBattleSelected = False
                                self.huntOrBattle = "hunt"
                                self.hb = 0
                                self.battleQuestValue = None
                                self.tempBattleQuestValue = None
                        elif autoBattle:
                            self.tempahuntQuestValue+=1
                            if self.huntQuestValue <= self.tempBattleQuestValue:
                                self.huntOrBattleSelected = False
                                self.huntOrBattle = "battle"
                                self.hb = 1
                                self.battleQuestValue = None
                                self.tempBattleQuestValue = None
                    if self.hb == 1 or self.huntOrBattleSelected:
                        await asyncio.sleep(random.uniform(huntOrBattleCooldown[0], huntOrBattleCooldown[1]))
                    else:
                        await asyncio.sleep(random.uniform(0.72667373732, 1.9439393929))
            except Exception as e:
                print(e)
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
            
    #pray/curse
    # QuestsList = [userid,messageChannel,guildId, [questType,questsProgress]]
    @tasks.loop()
    async def send_curse_and_prayer(self):
        try:
            if self.justStarted:
                await asyncio.sleep(random.uniform(0.93535353, 1.726364646))
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))        
            if self.f != True and self.sleep != True:
                if userToPrayOrCurse and self.user.id != userToPrayOrCurse:
                    self.current_time = time.time()
                    self.time_since_last_cmd = self.current_time - self.last_cmd_time
                    if self.tempPrayOrCurse == []:
                        #await self.cm.send(f'{setprefix}{self.prayOrCurse} <@{userToPrayOrCurse}>')
                        await self.sendCommands(channel=self.cm, message=f"{setprefix}{self.prayOrCurse} <@{userToPrayOrCurse}>", typing=typingIndicator)
                        #print("acc2")
                    else:
                        #await self.cm.send(f'{setprefix}{self.tempPrayOrCurse[1]} <@{self.tempPrayOrCurse[0]}>')
                        await self.sendCommands(channel=self.cm, message=f"{setprefix}{self.tempPrayOrCurse[1]} <@{self.tempPrayOrCurse[0]}>", typing=typingIndicator)
                        #self.tempPrayOrCurse[1]-=1                    
                        for o,i in enumerate(questsList):
                            if i[0] == self.tempPrayOrCurse[0]: #userid
                                for z,x in questsList[o][3]: #[questType,questsProgress]]
                                    if x[0] == self.tempPrayOrCurse[1]: #questType
                                        questsList[o][3][z][1] -= 1
                                        if questsList[o][3][z][1] == 0:
                                            questsList[o][3].pop(z)
                                            break                   
                    self.lastcmd = self.prayOrCurse
                    self.last_cmd_time = time.time()
                else:
                    if self.tempPrayOrCurse == []:
                        #await self.cm.send(f'{setprefix}{self.prayOrCurse}')
                        await self.sendCommands(channel=self.cm, message=f"{setprefix}{self.prayOrCurse}", typing=typingIndicator)
                        #print("acc")
                    else:
                        #await self.cm.send(f'{setprefix}{self.tempPrayOrCurse[1]} <@{self.tempPrayOrCurse[0]}>')
                        await self.sendCommands(channel=self.cm, message=f"{setprefix}{self.tempPrayOrCurse[1]} <@{self.tempPrayOrCurse[0]}>", typing=typingIndicator)
                        #self.tempPrayOrCurse[1]-=1                    
                        for o,i in enumerate(questsList):
                            if i[0] == self.tempPrayOrCurse[0]: #userid
                                for z,x in questsList[o][3]: #[questType,questsProgress]]
                                    if x[0] == self.tempPrayOrCurse[1]: #questType
                                        questsList[o][3][z][1] -= 1
                                        if questsList[o][3][z][1] == 0:
                                            questsList[o][3].pop(z)
                                            break  
                    self.lastcmd = self.prayOrCurse
                    self.last_cmd_time = time.time()
                console.print(f"-{self.user}[+] ran {self.prayOrCurse}.".center(console_width - 2 ), style = "magenta on black")
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[+] ran {self.prayOrCurse}.")
                await asyncio.sleep(random.uniform(prayOrCurseCooldown[0], prayOrCurseCooldown[1]))
            else:
                await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
        except Exception as e:
            print(e, "pray")
     # Coinflip
    @tasks.loop()
    async def send_cf(self):
        try:
            if self.f != True and self.sleep != True:
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.gambleCashCheck[0] == self.cfLastAmt and self.cfLastAmt != gambleStartValue:
                    self.gambleCashCheck2[0]+=1
                    if self.gambleCashCheck2[0] == 2:
                        console.print(f"-{self.user}[–] Stopping coinflip ‐ No Cash".center(console_width - 2 ), style = "red on black")
                        if webhookEnabled:
                            webhookSender(f"-{self.user}[–] Stopping coinflip ‐ No Cash.")
                        self.send_cf.stop()
                else:
                    self.gambleCashCheck[0] = self.cfLastAmt
                if self.cfLastAmt >= 250000:
                    console.print(f"-{self.user}[–] Stopping coinflip ‐ 250k exceeded".center(console_width - 2 ), style = "red on black")
                    if webhookEnabled:
                        webhookSender(f"-{self.user}[–] Stopping coinflip ‐ 250k exceeded.")
                    self.send_cf.stop()
                    return
                elif 0 >= self.gambleTotal:
                    if webhookEnabled:
                        webhookSender(f"-{self.user}[–] Stopping All Gambling. ‐ allotted value exceeded.")
                    console.print(f"-{self.user}[–] Stopping coinflip ‐ allotted value exceeded".center(console_width - 2 ), style = "red on black")
                    self.send_slots.stop()
                    self.send_cf.stop()
                    return
                    #add bj here...
                #await self.cm.send(f'{setprefix}cf {self.cfLastAmt}')
                await self.sendCommands(channel=self.cm, message=f"{setprefix}cf {self.cfLastAmt} {random.choice(cfOptions)[0]}", typing=typingIndicator)
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[–] ran Coinflip")
                console.print(f"-{self.user}[+] ran Coinflip.".center(console_width - 2 ), style = "cyan on black")
                await asyncio.sleep(random.uniform(gambleCd[0], gambleCd[1]))
        except Exception as e:
            print(e)
    # Slots    
    @tasks.loop()
    async def send_slots(self):
        if self.f != True and self.sleep != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.gambleCashCheck[1] == self.slotsLastAmt and self.slotsLastAmt != gambleStartValue:
                self.gambleCashCheck2[1]+=1
                if self.gambleCashCheck2[1] == 2:
                    console.print(f"-{self.user}[–] Stopping slots ‐ No Cash".center(console_width - 2 ), style = "red on black")
                    if webhookEnabled:
                        webhookSender(f"-{self.user}[–] Stopping slots ‐ No Cash.")
                    self.send_slots.stop()
            else:
                self.gambleCashCheck[0] = self.slotsLastAmt
            if self.slotsLastAmt >= 250000:
                if webhookEnabled:
                    webhookSender(f"-{self.user}[–] Stopping slots ‐ 250k exceeded.")
                console.print(f"-{self.user}[–] Stopping slots ‐ 250k exceeded".center(console_width - 2 ), style = "red on black")
                self.send_slots.stop()
                return
            elif 0 >= self.gambleTotal:
                if webhookEnabled:
                    webhookSender(f"-{self.user}[–] Stopping all Gambling. ‐ allotted value exceeded.")
                console.print(f"-{self.user}[–] Stopping all Gambling. ‐ allotted value exceeded".center(console_width - 2 ), style = "red on black")
                self.send_slots.stop()
                self.send_cf.stop()
                return
                #add bj here...
            #await self.cm.send(f'{setprefix}slots {self.slotsLastAmt}')
            await self.sendCommands(channel=self.cm, message=f"{setprefix}slots {self.slotsLastAmt}", typing=typingIndicator)
            if webhookUselessLog:
                webhookSender(f"-{self.user}[‐] ran Slots")
            console.print(f"-{self.user}[+] ran Slots.".center(console_width - 2 ), style = "cyan on black")
            await asyncio.sleep(random.uniform(gambleCd[0], gambleCd[1]))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     # Owo top
    @tasks.loop()
    async def send_owo(self):
        if self.f != True and self.sleep != True:
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            #await self.cm.send('owo')
            await self.sendCommands(channel=self.cm, message="owo", typing=typingIndicator)
            self.last_cmd_time = time.time()
            console.print(f"-{self.user}[+] ran OwO".center(console_width - 2 ), style = "Cyan on black")
            if webhookUselessLog:
                webhookSender(f"-{self.user}[–] ran OwO")
            if autoOwo == False:
                self.owoCount+=1 
                if self.owoCount >= self.owoCountGoal:
                    #self.owoQuest = False
                    self.send_owo.stop()
            await asyncio.sleep(random.uniform(11.28288282, 19.928292929))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    #shop
    @tasks.loop()
    async def buyItems(self):
        if self.f != True and self.sleep != True:
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            #await self.cm.send('owo')
            if self.shopCheck[0] != True:
                if self.shopCheck[2]:
                    console.print(f"-{self.user}[–] disabling shop as user doesn't have enough cash".center(console_width - 2 ), style = "red on black")
                    self.buyItems.stop()
                    self.shopCheck = [True, None, False]
                else:
                    self.shopCheck[2] = True
            self.shopCheck[0] = False
            self.shopCheck[1] = random.choice(shopItemsToBuy) # This will be made use of later for improved shop buy
            await self.sendCommands(channel=self.cm, message=f"{setprefix}buy {self.shopCheck[1]}", typing=typingIndicator)
            self.last_cmd_time = time.time()
            console.print(f"-{self.user}[+] brought item(s) from shop".center(console_width - 2 ), style = "Cyan on black")
            if webhookUselessLog:
                webhookSender(f"-{self.user}[–] brought item(s) from shop")
            await asyncio.sleep(random.uniform(shopCd[0], shopCd[1]))
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
                self.broke[1] = False
        if self.f != True and self.sleep != True:
            self.current_time = time.time()
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            #await self.cm.send(f'{setprefix}{self.sellOrSac} {rarity}')
            await self.sendCommands(channel=self.cm, message=f"{setprefix}{self.sellOrSac} {rarity}", typing=typingIndicator)
            self.last_cmd_time = time.time()
            if webhookEnabled:
                webhookSender(f"-{self.user}[+] ran {self.sellOrSac}")
            console.print(f"-{self.user}[+] ran {self.sellOrSac}".center(console_width - 2 ), style = "Cyan on black")
            await asyncio.sleep(random.uniform(sellOrSacCooldown[0], sellOrSacCooldown[1]))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     # Custom commands
    @tasks.loop(seconds=1)
    async def send_custom(self):
        try:
            self.tasks = [self.send_command_custom(cmd, cd) for cmd, cd in zip(sorted_list1, sorted_list2)]
            await asyncio.gather(*self.tasks)
        except Exception as e:
            print("send_custom error", e)
        while self.f or self.sleep:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    # Quests
    @tasks.loop()
    async def check_quests(self):
        if self.f != True and self.sleep != True:
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            #await self.cm.send(f'{setprefix}quest')
            await self.sendCommands(channel=self.cm, message=f"{setprefix}quest", typing=typingIndicator)
            console.print(f"-{self.user}[+] checking quest status...".center(console_width - 2 ), style = "green on black")
            self.last_cmd_time = time.time()
            await asyncio.sleep(random.uniform(300.28288282, 351.928292929))
            if self.questsDone:
                #self.current_time = time.time()
                #self.time_since_last_cmd = self.current_time - self.last_cmd_time
                self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
                self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst       
                self.formatted_time = "{:02}h {:02}m {:02}s".format(
                    int(self.time_until_12am_pst.total_seconds() // 3600),
                    int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
                    int(self.time_until_12am_pst.total_seconds() % 60)
            )
                self.total_seconds = self.time_until_12am_pst.total_seconds()
                await asyncio.sleep(self.total_seconds + random.uniform(34.377337,93.7473737))
                self.questsDone = False
        else:        
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    # Quest Handler
    @tasks.loop()
    async def questHandler(self):
        try:
            if self.f != True and self.sleep != True:
                print("questHandler started", self.user)
                await asyncio.sleep(random.uniform(10.3389,20.399))
                #print("questHandler running", self.user)
                # QuestsList = [userid,messageChannel,guildId, [questType,questsProgress]]
                if questsList != []:
                    for y,i in enumerate(questsList):
                        if i[2] == self.cm.guild.id:
                            for o,x in enumerate(i[3]):
                                if x[0] == "pray":
                                    print("qpray")
                                    if self.send_curse_and_prayer.is_running():
                                        if autoPray or autoCurse:
                                            if self.tempPrayOrCurse == []:
                                                self.tempPrayOrCurse = [i[0], x[0]]
                                                print(self.tempPrayOrCurse)
                                        else:
                                            self.current_time = time.time()
                                            self.time_since_last_cmd = self.current_time - self.last_cmd_time
                                            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                                                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                                            #await self.cm.send(f"{setprefix}pray <@{i[0]}>")
                                            await self.sendCommands(channel=self.cm, message=f"{setprefix}pray <@{i[0]}>", typing=typingIndicator)
                                            self.last_cmd_time = time.time()
                                            questsList[y][3][o][1]-=1
                                            if questsList[y][3][o][1] == 0:
                                                questsList[y][3].pop(o)
                                                self.prayBy = False
                                elif x[0] == "curse":
                                    print("qcurse")
                                    if self.send_curse_and_prayer.is_running():
                                        if autoPray or autoCurse:
                                            if self.tempPrayOrCurse == []:
                                                self.tempPrayOrCurse = [i[0], x[0]]
                                        else:
                                            self.current_time = time.time()
                                            self.time_since_last_cmd = self.current_time - self.last_cmd_time
                                            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                                                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                                            #await self.cm.send(f'''{setprefix}curse <@{i[0]}>''')
                                            await self.sendCommands(channel=self.cm, message=f"{setprefix}curse <@{i[0]}>", typing=typingIndicator)
                                            print("lsss goooo!")
                                            self.last_cmd_time = time.time()
                                            questsList[y][3][o][1]-=1
                                            if questsList[y][3][o][1] == 0:
                                                questsList[y][3].pop(o)
                                                self.curseBy = False
                                elif x[0] == "cookie":
                                    print("qcookie")
                                    self.current_time = time.time()
                                    self.time_since_last_cmd = self.current_time - self.last_cmd_time
                                    if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                                        await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                                    self.tempCookie = i[0]
                                    if not cookie:
                                        #await self.cm.send(f"{setprefix}rep <@{self.tempCookie}>")
                                        await self.sendCommands(channel=self.cm, message=f"{setprefix}rep <@{self.tempCookie}>", typing=typingIndicator)
                                    self.last_cmd_time = time.time()
                                    questsList[y][3][o][1]-=1
                                    if questsList[y][3][o][1] == 0:
                                        questsList[y][3].pop(o)
                                        self.repBy = False
                                elif x[0] == "action":
                                    print("qaction")
                                    self.current_time = time.time()
                                    self.time_since_last_cmd = self.current_time - self.last_cmd_time
                                    if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                                        await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                                    #await self.cm.send(f'''{setprefix}{random.choice(["wave","pet","nom","poke","greet","kill","handholding","punch"])} <@{i[0]}>''')
                                    await self.sendCommands(channel=self.cm, message=f"""{setprefix}{random.choice(["wave","pet","nom","poke","greet","kill","handholding","punch"])} <@{i[0]}>""", typing=typingIndicator)
                                    self.last_cmd_time = time.time()
                                    questsList[y][3][o][1]-=1
                                    if questsList[y][3][o][1] == 0:
                                        questsList[y][3].pop(o)
                                        self.emoteby = False
                await asyncio.sleep(random.uniform(150.12667373732, 360.9439393929))
            else:        
                await asyncio.sleep(random.uniform(3.12667373732, 6.9439393929))
        except Exception as e:
            print(e, "quest handler")
            #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
  # Lottery
    @tasks.loop()
    async def send_lottery(self):
        if self.f != True and self.sleep != True:
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.5 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.last_cmd_time = time.time()
            #await self.cm.send(f'{setprefix}lottery {lotteryAmt}')
            await self.sendCommands(channel=self.cm, message=f"{setprefix}lottery {lotteryAmt}", typing=typingIndicator)
            self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
            self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst       
            self.formatted_time = "{:02}h {:02}m {:02}s".format(
                int(self.time_until_12am_pst.total_seconds() // 3600),
                int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
                int(self.time_until_12am_pst.total_seconds() % 60)
        )
            self.total_seconds = self.time_until_12am_pst.total_seconds()
            console.print(f"-{self.user}[+] ran lottery. {self.total_seconds}".center(console_width - 2 ), style = "cyan on black")
            if webhookEnabled:
                webhookSender(f"-{self.user}[+] ran lottery.", f"Running Lottery again in {self.total_seconds}")
            await asyncio.sleep(self.total_seconds + random.uniform(34.377337,93.7473737))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     # Lvl grind
    @tasks.loop()
    async def lvlGrind(self):
        if self.f != True and self.sleep != True:
            if useQuoteInstead:
                #print("somewhat working")
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(quotesUrl) as response:
                            if response.status == 200:
                                data = await response.json()
                                #print(data)
                                self.quote = data[0]["quote"]
                                #await self.cm.send(self.quote)
                                await self.sendCommands(channel=self.cm, message=self.quote, typing=typingIndicator)
                                console.print(f"-{self.user}[+] Send random quote(lvl grind)".center(console_width - 2 ), style = "purple3 on black")
                                if webhookEnabled:
                                    webhookSender(f"-{self.user}[+] send random quote.", "This is for level grind")                                
                            else:
                                #await self.cm.send(generate_random_string())
                                await self.sendCommands(channel=self.cm, message=generate_random_string(), typing=typingIndicator)
                                console.print(f"-{self.user}[+] Send random strings(lvl grind)".center(console_width - 2 ), style = "purple3 on black")
                                if webhookEnabled:
                                    webhookSender(f"-{self.user}[+] send random strings.", "This is for level grind")                                
                except Exception as e:
                    print(e)
            else:
                #await self.cm.send(generate_random_string()) # Better than sending quotes(In my opinion).
                await self.sendCommands(channel=self.cm, message=generate_random_string(), typing=typingIndicator)
                console.print(f"-{self.user}[+] Send random strings(lvl grind)".center(console_width - 2 ), style = "purple3 on black")
                if webhookEnabled:
                    webhookSender(f"-{self.user}[+] send random strings.", "This is for level grind")
            await asyncio.sleep(random.uniform(lvlGrindCooldown[0], lvlGrindCooldown[1]))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    # cookie
    @tasks.loop()
    async def send_cookie(self):
        if self.f != True and self.sleep != True:
            if self.tempCookie != None:
                for o,i in enumerate(questsList):
                    if i[0] == self.tempCookie: #userid
                        for z,x in questsList[o][3]: #[questType,questsProgress]]
                            if x[0] == "cookie": #questType                                    
                                questsList[o][3][x][1]-=1
                                if questsList[o][3][x][1]:
                                    questsList[o][3].pop(x)
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            if self.tempCookie != None:
                #await self.cm.send(f'{setprefix}cookie {self.tempCookie}')
                await self.sendCommands(channel=self.cm, message=f"{setprefix}cookie {self.tempCookie}", typing=typingIndicator)
            else:
                #await self.cm.send(f'{setprefix}cookie {cookieUserId}')
                await self.sendCommands(channel=self.cm, message=f"{setprefix}cookie {cookieUserId}", typing=typingIndicator)
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
            if webhookEnabled:
                webhookSender(f"-{self.user}[+] send cookie.", f"Trying cookie again in {self.total_seconds}")
            console.print(f"-{self.user}[+] send cookie. {self.total_seconds}".center(console_width - 2 ), style = "cyan on black")
            await asyncio.sleep(self.total_seconds + random.uniform(34.377337,93.7473737))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
            
     # emoteTo {Quest}
    @tasks.loop()
    async def emoteTo(self):
        if self.f != True and self.sleep != True:
            if self.emoteCount >= self.emoteCountGoal:
                self.emoteTo.stop()
            self.last_cmd_time = time.time()
            self.current_time = time.time()
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            #await self.cm.send(f'{setprefix}{random.choice(["wave","pet","nom","poke","greet","kill","handholding","punch"])} <@408785106942164992>')
            await self.sendCommands(channel=self.cm, message=f'{setprefix}{random.choice(["wave","pet","nom","poke","greet","kill","handholding","punch"])} <@408785106942164992>', typing=typingIndicator)
            self.emoteCount+=1
            self.last_cmd_time = time.time()
            console.print(f"-{self.user}[+] Send random emotes(quest)".center(console_width - 2 ), style = "purple3 on black")
            if webhookEnabled:
                webhookSender(f"-{self.user}[+] send emotes.", "This is for auto quest")
            await asyncio.sleep(random.uniform(17.83727372,20.73891948))
        else:
            await asyncio.sleep(random.uniform(14.3838383, 20.9439393929))
     # gamble {Quest}
    @tasks.loop()
    async def send_gamble(self):
        if self.gambleCount >= self.gambleCountGoal:
            self.send_gamble.stop()
        if self.f != True and self.sleep != True:
            while self.gambleCount != self.gambleCountGoal:
                self.last_cmd_time = time.time()
                self.current_time = time.time()
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
                #await self.cm.send(f"{setprefix}cf 1")
                await self.sendCommands(channel=self.cm, message=f"{setprefix}cf 1", typing=typingIndicator)
                self.last_cmd_time = time.time()
                self.gambleCount+=1
                await asyncio.sleep(random.uniform(0.83727372,2.73891948))
                self.last_cmd_time = time.time()
                self.current_time = time.time()
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
                #await self.cm.send(f"{setprefix}slots 1")
                await self.sendCommands(channel=self.cm, message=f"{setprefix}slots 1", typing=typingIndicator)
                self.last_cmd_time = time.time()
                self.gambleCount+=1
                await asyncio.sleep(random.uniform(17.83727372,20.73891948))
        else:
            await asyncio.sleep(random.uniform(3.83727372,5.73891948))
    @tasks.loop(seconds=30)
    async def presence(self):
        if offline and self.status != discord.Status.invisible:
            try:
                #print(self.user)
                await self.change_presence(
                status=discord.Status.invisible, activity=self.activity
            )
                self.presence.stop()
            except:
                pass
        else:
            #print(self.user, "off", self.status)
            self.presence.stop()

    @presence.before_loop
    async def before_presence(self):
        await self.wait_until_ready()
#----------ON READY----------#
    async def on_ready(self):
        self.on_ready_dn = False
        self.cmds = 1
        self.cmds_cooldown = 0
        printBox(f'-Loaded {self.user.name}[*].'.center(console_width - 2 ),'bold purple on black' )
        listUserIds.append(self.user.id)
        await asyncio.sleep(0.12)
        try:
            self.cm = self.get_channel(self.channel_id)
            #qtemp.append(self.cm.guild.id)
        except Exception as e:
            print(e)
        try:
            self.dm = await self.fetch_user(408785106942164992)
        except Exception as e:
            print(e)
        if self.dm == None:
            print("channel disabled")
        self.presence.start()
        self.list_channel.append(self.dm.dm_channel.id)
        self.broke = [False, False] #check, confirmed
        # AUTO QUEST
        self.questsDone = False
        self.emoteby = False
        self.repBy = False
        self.prayBy = False
        self.curseBy = False
        self.owoChnl = False
        self.zooCheckReq = False
        self.questProgress= []
        self.questToDo = []
        self.tempPrayOrCurse = []
        self.questsList = []
        self.questsListInt = None
        self.battleQuestValue = None
        self.huntQuestValue = None
        #-------
        self.hunt = None
        self.webInt = None
        self.webSend = False
        self.tempHuntDisable = False
        self.battle = None
        self.justStarted = True
        self.list_channel = [self.channel_id, self.dm.dm_channel.id]
        if askForHelp:
            try:
                self.questChannel = self.get_channel(askForHelpChannel)
                print(self.questChannel.name, self.user)
                console.print(f"-{self.user}[~] Quests Help channel {self.questChannel.name} has been fetched!".center(console_width - 2 ), style = "medium_purple3 on black")
            except:
                self.questChannel = None
                console.print(f"-{self.user}[!] Failed to get channel with channelid {askForHelpChannel}".center(console_width - 2 ), style = "medium_purple3 on black")
        # [Coinflip, Slots]
        self.gambleCashCheck = [0,0]
        self.gambleCashCheck2 = [0,0]
        #---
        self.shopCheck = [True, None, False]
        self.last_cmd_time = 0
        self.lastcmd = None
        self.busy = False
        self.hb = 0
        self.lastHb = None
        self.ss = 0
        self.time_since_last_cmd = 0
        self.tempForCheck = False
        self.f = False
        self.zooCheckRecieved = False
        self.captchaType = None
        self.sleep = False
        self.changedPrefix = False
        # AutoGems
        self.gemHuntCnt = None
        self.gemEmpCnt = None
        self.gemLuckCnt = None
        self.gemSpecialCnt = None
        self.gems = autoGem
        self.invCheck = False
        #-------
        self.gambleTotal = gambleAllottedAmount
        
        # List for running loops randomly
        self.task_methods = []
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
            #self.send_hunt_or_battle.start()
            self.task_methods.append(self.send_hunt_or_battle.start)
         # Starting curse/pray loop
        if autoCurse or autoPray:
            if autoCurse:
                self.prayOrCurse = "curse"
            else:
                self.prayOrCurse = "pray"
            self.task_methods.append(self.send_curse_and_prayer.start)
        # Starting Daily loop
        if autoDaily:
            self.task_methods.append(self.send_daily.start)
        # start shop
        if shopEnabled:
            self.task_methods.append(self.buyItems.start)
        # Starting Auto Owo
        if autoOwo:
            self.task_methods.append(self.send_owo.start)
            #self.send_owo.start()
        await asyncio.sleep(random.uniform(2.4,6.8))
        if cookie:
            self.task_methods.append(self.send_cookie.start)
        # Starting Coinflip
        if autoCf:
            if doubleOnLose:
                self.cfMulti = 2
            else:
                self.cfMulti = 1
            self.cfLastAmt = gambleStartValue
            self.task_methods.append(self.send_cf.start)
        # Starting slots CHEXK
        if autoSlots:
            if doubleOnLose:
                self.slotsMulti = 2
            else:
                self.slotsMulti = 1
            self.slotsLastAmt = gambleStartValue
            self.task_methods.append(self.send_slots.start)
        # Random Breaks
        if sleepEnabled:
            self.random_account_sleeper.start()
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
            #self.send_sell_or_sac.start()
            self.task_methods.append(self.send_sell_or_sac.start)
        if customCommands:
            #self.send_custom.start()
            self.task_methods.append(self.send_custom.start)
        if autoQuest:
            self.questHandler.start()
            self.task_methods.append(self.check_quests.start)
        if lottery:
            #self.send_lottery.start()
            self.task_methods.append(self.send_lottery.start)
        if lvlGrind:
            self.task_methods.append(self.lvlGrind.start)
        random.shuffle(self.task_methods)
        for task_method in self.task_methods:
            task_method()
            await asyncio.sleep(random.uniform(0.4,0.8))
        embed1 = discord.Embed(
            title='logging in',
            description=f'logged in as {self.user.name}',
            color=discord.Color.dark_green()
        )
        if webhookEnabled:
            dwebhook.send(embed=embed1, username='uwu bot') 
        await asyncio.sleep(random.uniform(2.69,3.69))
        self.justStarted = False
        await asyncio.sleep(random.uniform(10, 30)) 
        self.delayCheck.start()
        #self.sleep = True
        #print("rr")
             
#----------ON MESSAGE----------#
    async def on_message(self, message):
        if not self.on_ready_dn:
            return
        if message.author.id != 408785106942164992:
            return
        #print(message.channel, message.channel.name)
        if "I have verified that you are human! Thank you! :3" in message.content and message.channel.id in self.list_channel:
            console.print(f"-{self.user}[+] Captcha solved. restarting...".center(console_width - 2 ), style = "dark_magenta on black")
            await asyncio.sleep(random.uniform(0.69, 2.69))
            self.f = False
            if webhookEnabled:
                webhookSender(f"-{self.user}[+] Captcha solved. restarting...")
            print(f'int {self.webInt} bool(webSend) {self.webSend} -- {self.user}')
            if websiteEnabled and self.webInt != None:
                print("attempting to pop captcha indirectly")
                while True:
                    self.tempListCount = 0
                    self.popped = False
                    for i in captchas:
                        if i == self.tempJsonData:
                            captchas.pop(self.tempListCount)
                            captchaAnswers.pop(self.tempListCount)
                            print("popped captcha indirectly")
                            self.popped = True
                            break
                        self.tempListCount+=1
                    if self.popped:
                        break
                    #print("looping while")
                print(captchas , captchaAnswers)
                self.webInt = None
                    
                self.captchaSolver.stop()
                self.webSend = False
                print(f'int {self.webInt} bool(webSend) {self.webSend} -- {self.user} after solving')
                print(f"{self.user} stopped captcha solver")
            return
        if any(b in message.content.lower() for b in list_captcha) and message.channel.id in self.list_channel:
            try:
                if list_captcha[1] in message.content:
                    self.captchaType = "link"
                else:
                    self.captchaType = "image"
                self.f = True
                self.captcha_channel_name = get_channel_name(message.channel)
                if termuxNotificationEnabled: #8ln from here
                    run_system_command(f"termux-notification -c '{notificationCaptchaContent.format(username=self.user.name,channelname=self.captcha_channel_name,captchatype=self.captchaType)}'", timeout=5, retry=True)
                if termuxToastEnabled:
                    run_system_command(f"termux-toast -c {toastTextColor} -b {toastBgColor} '{toastCaptchaContent.format(username=self.user.name,channelname=self.captcha_channel_name,captchatype=self.captchaType)}'", timeout=5, retry=True)
                console.print(f"-{self.user}[!] CAPTCHA DETECTED in {self.captcha_channel_name} waiting...".center(console_width - 2), style="deep_pink2 on black")
                embed2 = discord.Embed(
                    title=f'CAPTCHA :- {self.user} ;<',
                    description=f"user got captcha :- {self.user} ;<",
                    color=discord.Color.red()
                )
                if webhookEnabled:
                    if webhookCaptchaChnl:
                        self.webhook = SyncWebhook.from_url(webhookCaptchaChnl)
                        if webhookPingId:
                            self.webhook.send(content=f"<@webhookPingId>",embed=embed2, username='uwu bot warnings')
                        else:
                            self.webhook.send(embed=embed2, username='uwu bot warnings')
                    else:
                        if webhookPingId:
                            dwebhook.send(content=f"<@webhookPingId>",embed=embed2, username='uwu bot warnings')
                        else:
                            dwebhook.send(embed=embed2, username='uwu bot warnings')
                if termuxVibrationEnabled:
                    run_system_command(f"termux-vibrate -d {termuxVibrationTime}", timeout=5, retry=True) 
                if termuxAudioPlayer:
                    run_system_command(f"termux-media-player play {termuxAudioPlayerPath}", timeout=5, retry=True)
                if termuxTtsEnabled:
                    run_system_command(f"termux-tts-speak {termuxTtsContent}", timeout=7, retry=False)
                if desktopNotificationEnabled:
                    notification.notify(
                        title=f'{self.user}  DETECTED CAPTCHA',
                        message=desktopNotificationCaptchaContent.format(username=self.user.name,channelname=self.captcha_channel_name,captchatype=self.captchaType),
                        app_icon=None,
                        timeout=15,
                    )
                if captchaConsoleEnabled:
                    run_system_command(captchaConsoleContent, timeout=7, retry=False)
                if self.webSend == False and websiteEnabled:
                    try:
                        if list_captcha[1] in message.content:
                            self.dataToSend = {
                                "type": "link",
                                "url": "https://owobot.com/captcha",
                                "username": self.user.name
                            }
                        elif message.attachments:
                            if message.attachments[0].url is not None:
                                self.dataToSend = {
                                    "type": "image",
                                    "url": str(message.attachments[0].url),
                                    "username": self.user.name
                                }
                                self.captchaSolver.start()
                                self.webSend = True
                    except Exception as e:
                        print(f"error when attempting to send captcha to web {e}, for {self.user}")
                    try:
                        if self.webInt is None:
                            self.data_json = json.dumps(self.dataToSend)
                            self.curl_command = f'curl -X POST http://localhost:{websitePort}/add_captcha -H "Content-Type: application/json" -d \'{self.data_json}\' '
                            self.response_json = os.popen(self.curl_command).read()
                            self.response_dict = json.loads(self.response_json)
                            self.webInt = int(self.response_dict.get('status'))
                            self.tempJsonData = captchas[self.webInt]
                            print(self.webInt, "from curl post section")
                            print("captcha solver started")
                    except Exception as e:
                        print(f'Error when trying to get status :-> {e} Error for {self.user}')
                console.print(f"-{self.user}[!] Delay test successfully completed!.".center(console_width - 2), style="deep_pink2 on black")
                return
            except Exception as e:
                print(e)
        if "☠" in message.content and "You have been banned for" in message.content and message.channel.id in self.list_channel:
            self.f = True
            self.captcha_channel_name = get_channel_name(message.channel)
            if termuxNotificationEnabled: #8ln from here
                run_system_command(f"termux-notification -c '{notificationBannedContent.format(username=self.user.name,channelname=self.captcha_channel_name,captchatype='Banned')}'", timeout=5, retry=True)
            if termuxToastEnabled:
                run_system_command(f"termux-toast -c {toastTextColor} -b {toastBgColor} '{toastBannedContent.format(username=self.user.name,channelname=self.captcha_channel_name,captchatype='Banned')}'", timeout=5, retry=True)
            console.print(f"-{self.user}[!] BAN DETECTED.".center(console_width - 2 ), style = "deep_pink2 on black")
            embed2 = discord.Embed(
                    title=f'BANNED IN OWO :- {self.user} ;<',
                    description=f"user got banned :- {self.user} ;<",
                    color=discord.Color.red()
                                )
            if webhookEnabled:
                if webhookCaptchaChnl:
                    self.webhook = SyncWebhook.from_url(webhookCaptchaChnl)
                    if webhookPingId:
                        self.webhook.send(content=f"<@webhookPingId> , ",embed=embed2, username='uwu bot warnings')
                    else:
                        self.webhook.send(embed=embed2, username='uwu bot warnings')
                else:
                    if webhookPingId:
                        dwebhook.send(content=f"<@webhookPingId> , ",embed=embed2, username='uwu bot warnings')
                    else:
                        dwebhook.send(embed=embed2, username='uwu bot warnings')
            if termuxVibrationEnabled:
                run_system_command(f"termux-vibrate -d {termuxVibrationTime}", timeout=5, retry=True)
            if termuxAudioPlayer:
                run_system_command(f"termux-media-player play {termuxAudioPlayerPath}", timeout=5, retry=True)
            if desktopAudioPlayer:
                playsound(desktopAudioPlayerPath)
            if termuxTtsEnabled:
                run_system_command(f"termux-tts-speak A user got banned", timeout=7, retry=False)
            if banConsoleEnabled:
                run_system_command(banConsoleContent, timeout=7, retry=False)
            # temp disabled tts
            if desktopNotificationEnabled:
                notification.notify(
                    title = f'{self.user}[!] User BANNED in OwO!!',
                    message = desktopNotificationBannedContent.format(username=self.user.name,channelname=self.captcha_channel_name,captchatype="Banned"),
                    app_icon = None,
                    timeout = 15,
                    )
            console.print(f"-{self.user}[!] Delay test successfully completed!.".center(console_width - 2 ), style = "deep_pink2 on black")
            return
        if message.channel.id == self.channel_id and "**You must accept these rules to use the bot!**" in message.content.lower():
            await asyncio.sleep(random.uniform(0.6,1.7))
            try:
                await message.components[0].children[0].click()
            except:
                pass
        if message.channel.id == self.channel_id and ('you found' in message.content.lower() or "caught" in message.content.lower()):
            try:
                self.hb = 1
                self.last_cmd_time = time.time()
                self.lastcmd = "hunt"
                self.broke = [False,False]
                if "caught" in message.content.lower() and self.gems:
                    if self.f:
                        return
                    print("test")
                    self.current_time = time.time()
                    if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                        await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                    #await self.cm.send(f"{setprefix}inventory")
                    await self.sendCommands(channel=self.cm, message=f"{setprefix}inventory", typing=typingIndicator)
                    console.print(f"-{self.user}[~] checking Inventory....".center(console_width - 2 ), style = "Cyan on black")
                    if webhookUselessLog:
                        webhookSender(f"-{self.user}[~] checking Inventory.", "For autoGem..")
                    self.invCheck = True
            except Exception as e:
                print(e)
        if message.channel.id == self.channel_id and "`battle` and `hunt` cooldowns have increased to prevent rateLimits issues." in message.content:
            if huntOrBattleCooldown < 20:
                huntOrBattleCooldown+=10
                console.print(f"-{self.user}[–] Increasing hunt and battle cooldowns since owo is having ratelimits...".center(console_width - 2 ), style = "red on black")
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[~] Cooldown for hunt and battle increased.", "OwO seems to have enabled cooldowns for hunt and battle due to ratelimits. Increasing sleep time to prevent spam...")
        if message.channel.id == self.channel_id and "You don't have enough cowoncy!" in message.content:
            self.broke[0] = True
            console.print(f"-{self.user}[–] may disable hunt since not enough cash... checking..".center(console_width - 2 ), style = "red on black")
        if message.channel.id == self.channel_id and ("you found a **lootbox**!" in message.content.lower() or "you found a **weapon crate**!" in message.content.lower()):
            if self.f:
                return
            if "**lootbox**" in message.content.lower() and autoLootbox:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                #await self.cm.send(f"{setprefix}lb all")
                await self.sendCommands(channel=self.cm, message=f"{setprefix}lb all", typing=typingIndicator)
                console.print(f"-{self.user}[+] used lootbox".center(console_width - 2 ), style = "magenta on black")
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[+] used lootbox")
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
            elif "**weapon crate**" in message.content.lower() and autoCrate:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                #await self.cm.send(f"{setprefix}crate all")
                await self.sendCommands(channel=self.cm, message=f"{setprefix}crate all", typing=typingIndicator)
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[+] used crates")
                console.print(f"-{self.user}[+] used all crates".center(console_width - 2 ), style = "magenta on black")
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
        if message.channel.id == self.channel_id and "Create a team with the command `owo team add {animal}`" in message.content:
            try:
                console.print(f"-{self.user}[–] Missing team for battle... attempting to create one.".center(console_width - 2 ), style = "magenta on black")
                self.sleep = True
                self.zooCheckReq = True
                await self.sendCommands(channel=self.cm, message=f"{setprefix}zoo", typing=typingIndicator)
                await asyncio.sleep(random.uniform(1,2))
                if self.zooCheckRecieved:
                    self.zooCheckRecieved = False
                else:
                    self.sleep = False # To trigger command again, lazy to add better ways for now haha. This is temporary. – 14th Jun 2024
            except Exception as e:
                print(e)
        if self.zooCheckReq and  message.channel.id == self.channel_id and "s zoo! **" in message.content:
            self.zooCheckRecieved = True
            self.zooCheckReq = False
            self.animals = get_emoji_names(message.content)
            self.animals.reverse()
            print(self.animals)
            self.threeAnimals = min(len(self.animals), 3) #int
            for i in range(self.threeAnimals):
                await self.sendCommands(channel=self.cm, message=f"{setprefix}team add {self.animals[i]}", typing=typingIndicator)
                await asyncio.sleep(random.uniform(1.5,2.3))
            self.sleep = False 
        if shopEnabled and message.channel.id == self.channel_id and ", you bought a" in message.content:
            self.shopCheck[0] = True
        if message.channel.id == self.channel_id and "Inventory" in message.content and "=" in message.content.lower():
            if self.invCheck:
                self.invNumbers = re.findall(r'`(\d+)`', message.content)
                #self.tempHuntDisable = True
                self.sleep = True
                self.tempForCheck = False
                self.sendingGemsIds = ""
                self.gem_intent_mapping = {
                    0: (huntGems, autoHuntGem),
                    1: (empGems, autoEmpoweredGem),
                    2: (luckGems, autoLuckyGem),
                    3: (specialGems, autoSpecialGem)
                    }
                self.gem_match_count = {}
                for gem_list, gem_enabled in self.gem_intent_mapping.values():
                    if gem_enabled:
                        for gem in gem_list:
                            if gem in self.invNumbers:
                                self.gem_match_count[gem] = self.gem_match_count.get(gem, 0) + 1
                self.sorted_gems = sorted(self.gem_match_count.keys(), key=lambda x: self.gem_match_count[x], reverse=True)
                #self.added_gems = set()
                self.added_intents = set()
                for gem in self.sorted_gems:
                    for intent, (gem_list, gem_enabled) in self.gem_intent_mapping.items():
                        if gem_enabled and gem in gem_list and intent not in self.added_intents:
                            self.sendingGemsIds+=f"{gem} "
                            #self.added_gems.add(gem)
                            self.added_intents.add(intent)
                            break
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                self.tempForCheck = False
                #print(self.sendingGemsIds)
                if self.sendingGemsIds != "":
                    await self.sendCommands(channel=self.cm, message=f"{setprefix}use {self.sendingGemsIds}", typing=typingIndicator)
                    #await self.cm.send(f'{setprefix}use {self.sendingGemsIds}')
                    console.print(f"-{self.user}[+] used gems({self.sendingGemsIds})".center(console_width - 2 ), style = "Cyan on black")
                    if webhookUselessLog:
                        webhookSender(f"-{self.user}[+] used Gems({self.sendingGemsIds})")
                    self.last_cmd_time = time.time()
                else:
                    self.gems = False
                    console.print(f"-{self.user}[!] No gems to use... disabling...".center(console_width - 2 ), style = "deep_pink2 on black")
                self.invCheck = False
                #self.tempHuntDisable = False
                await asyncio.sleep(random.uniform(0.3,0.7))
                self.sleep = False
                self.sendingGemsIds = ""
        if message.embeds and message.channel.id == self.channel_id:
            for embed in message.embeds:
                if embed.author.name is not None and "goes into battle!" in embed.author.name.lower():
                    # Check to see if Hunt is completed or not.
                    self.hb = 0 #check
                    self.last_cmd_time = time.time()
                    self.lastcmd = "battle"
                if embed.author.name is not None and "quest log" in embed.author.name.lower():
                    if not autoQuest:
                        return
                    try:
                        self.questToDo = []
                        self.questProgress = []
                        for match in re.findall(r'Progress: \[(\d+)/(\d+)\]', embed.description):
                            x, y = match #split
                            #print(f'Progress: {x}/{y}')
                            self.questProgress.append(x)
                            self.questProgress.append(y)
                        #print(self.questProgress , self.user)
                        for match in re.findall(r'\*\*(.*?)\*\*', embed.description):
                            x = match
                            print(x)
                            #print(self.questToDo)
                            self.questToDo.append(x)
                        print(self.questToDo, self.user)
                        if "you finished all of your quests!" in embed.description.lower():
                            self.questsDone = True
                            self.owoChnl = False
                            self.emoteby = False
                            self.repBy = False
                            self.curseBy = False
                            self.prayBy = False
                            #dble check check system.
                            if self.send_gamble.is_running():
                                self.send_gamble.stop()
                            if not autoOwo:
                                if self.send_owo.is_running():
                                    self.send_owo.stop()
                            if self.emoteTo.is_running():
                                self.emoteTo.stop()
                            if doEvenIfDisabled:
                                if autoHunt == False and autoBattle == False:
                                    if send_hunt_or_battle.is_running():
                                        self.huntQuestValue = None
                                        self.battleQuestValue = None
                                        send_hunt_or_battle.stop()
                                elif autoHunt == False:
                                    self.huntOrBattleSelected = False
                                    self.huntOrBattle = "battle"
                                    self.hb = 1
                                    self.battleQuestValue = None
                                    self.tempBattleQuestValue = None
                                elif autoBattle == False:
                                    self.huntOrBattleSelected = False
                                    self.huntOrBattle = "hunt"
                                    self.hb = 0
                                    self.battleQuestValue = None
                                    self.tempBattleQuestValue = None
                            console.print(f"-{self.user}[+] Quests have been fully completed!!".center(console_width - 2 ), style = "medium_purple3 on black")
                            return
                    except Exception as e:
                        print("f quests", e)
                    for o,i in enumerate(self.questToDo):  # o = int, i = item     
                    #---------------------Temp Border---------------------#
                        #print(i,o)                    
                        if "Manually hunt" in i or "Hunt 3 animals that are " in i:
                            try:
                                if not autoHunt and doEvenIfDisabled:
                                    if "Hunt 3 animals that are " in i:
                                        self.huntQuestValue = None
                                        self.tempHuntQuestValue = None
                                    else:
                                        self.tempHuntQuestValue = 0
                                        self.huntQuestValue = int(self.questProgress[(o*2)+1]) - int(self.questProgress[o*2])
                                    if autoBattle:
                                        self.huntOrBattleSelected = False
                                        self.hb = 0
                                        self.huntOrBattle = "hunt"
                                    else:
                                        self.huntOrBattleSelected = True
                                        self.huntOrBattle = "hunt"
                                        self.hb = 0
                                        if not self.send_hunt_or_battle.is_running():
                                            self.send_hunt_or_battle.start()
                                #print("man h", self.user)
                            except Exception as e:
                                print(e, "man h")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        elif "Battle with a friend " in i:
                            print("battle with a friend detected, but disabled")
                        elif "Battle " in i:
                            try:
                                self.tempBattleQuestValue = 0
                                self.battleQuestValue = int(self.questProgress[(o*2)+1]) - int(self.questProgress[o*2])
                                if autoHunt:
                                    self.huntOrBattleSelected = False
                                    self.hb = 1
                                    self.huntOrBattle = "battle"
                                else:
                                    self.huntOrBattleSelected = True
                                    self.huntOrBattle = "battle"
                                    self.hb = 1
                                    if not self.send_hunt_or_battle.is_running():
                                        self.send_hunt_or_battle.start()          
                                #print("battle", self.user)
                            except Exception as e:
                                print(e, "battle")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        elif "Gamble " in i:
                            try:
                                self.gambleCount = 0
                                self.gambleCountGoal = int(self.questProgress[(o*2)+1]) - int(self.questProgress[o*2])
                                #self.gambleQuest = True
                                if self.send_gamble.is_running() == False and (autoCf == False and autoSlots == False): # add bj later
                                    self.send_gamble.start()
                                #print("gamble", self.user)
                            except Exception as e:
                                print(e, "gamble")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        elif "Say 'owo' " in i:
                            try:
                                self.owoCount = 0
                                self.owoCountGoal = int(self.questProgress[(o*2)+1]) - int(self.questProgress[o*2])
                                #self.owoQuest = True
                                if not self.send_owo.is_running():
                                    self.send_owo.start()
                                #print("say owo",self.user)
                            except Exception as e:
                                print(e,"owo q")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        elif "Use an action command on someone " in i:
                            try:
                                self.emoteCount = 0
                                self.emoteCountGoal = int(self.questProgress[(o*2)+1]) - int(self.questProgress[o*2])
                                if not self.emoteTo.is_running():
                                    self.emoteTo.start()
                                #print("action", self.user)
                            except Exception as e:
                                print(e, "action0")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        elif "Have a friend use an action command on you " in i:
                            try:
                                if token_len != 1:
                                    if self.emoteby == False:
                                        self.questsList.append(["action", int(self.questProgress[(o*2)+1]) - int(self.questProgress[o*2])])
                                        self.emoteby = True
                                #print("emoteBy", self.user)
                                if askForHelp and self.owoChnl == False and self.questChannel != None:
                                    #self.list_channel.append(self.owoSupportChannel.channel.id)
                                    self.current_time = time.time()
                                    self.time_since_last_cmd = self.current_time - self.last_cmd_time
                                    if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                                        await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                                    console.print(f"-{self.user}[~] Asking for help in {self.questChannel.name}".center(console_width - 2 ), style = "medium_purple3 on black")
                                    #await self.questChannel.send("owo quest")
                                    await self.sendCommands(channel=self.questChannel, message="owo quest", typing=typingIndicator)
                                    self.owoChnl = True
                            except Exception as e:
                                print(e, "action")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        elif "Receive a cookie from " in i:
                            try:
                            # repBy
                                #print(token_len)
                                if token_len != 1:
                                    if self.repBy == False:
                                        self.questsList.append(["cookie", int(self.questProgress[(o*2)+1]) - int(self.questProgress[o*2])])
                                        self.repBy = True
                                    if askForHelp and self.owoChnl == False and self.questChannel != None:
                                        self.current_time = time.time()
                                        self.time_since_last_cmd = self.current_time - self.last_cmd_time
                                        if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                                            await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                                        console.print(f"-{self.user}[~] Asking for help in {self.questChannel.name}".center(console_width - 2 ), style = "medium_purple3 on black")
                                        #await self.questChannel.send("owo quest")
                                        await self.sendCommands(channel=self.questChannel, message="owo quest", typing=typingIndicator)
                                        self.owoChnl = True
                            except Exception as e:
                                print(e, "cookie")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        elif "Have a friend pray to you " in i:
                            try:
                            # prayBy
                                if token_len != 1:
                                    if self.prayBy == False:
                                        self.questsList.append(["pray", int(self.questProgress[(o*2)+1]) - int(self.questProgress[o*2])])
                                        self.prayBy = True
                                #print("prayBy", self.user)
                                if askForHelp and self.owoChnl == False and self.questChannel != None:
                                    #self.list_channel.append(self.owoSupportChannel.channel.id)
                                    self.current_time = time.time()
                                    self.time_since_last_cmd = self.current_time - self.last_cmd_time
                                    if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                                        await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                                    console.print(f"-{self.user}[~] Asking for help in {self.questChannel.name}".center(console_width - 2 ), style = "medium_purple3 on black")
                                    #await self.questChannel.send("owo quest")
                                    await self.sendCommands(channel=self.questChannel, message="owo quest", typing=typingIndicator)
                                    self.owoChnl = True
                            except Exception as e:
                                print(e, "prayer")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        #print("proceedings 9")
                        elif "Have a friend curse you" in i:
                            # CurseBy
                            try:
                                if token_len != 1:
                                    if self.curseBy == False:
                                        self.questsList.append(["curse", int(self.questProgress[(o*2)+1]) - int(self.questProgress[o*2])])
                                        self.curseBy = True
                                #print("enabled curseBy", self.user)
                                if askForHelp and self.owoChnl == False and self.questChannel != None:
                                    #self.list_channel.append(self.owoSupportChannel.channel.id)
                                    self.current_time = time.time()
                                    self.time_since_last_cmd = self.current_time - self.last_cmd_time
                                    if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                                        await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                                    console.print(f"-{self.user}[~] Asking for help in {self.questChannel.name}".center(console_width - 2 ), style = "medium_purple3 on black")
                                    #await self.questChannel.send("owo quest")
                                    await self.sendCommands(channel=self.questChannel, message="owo quest", typing=typingIndicator)
                                    self.owoChnl = True
                            except Exception as e:
                                print(e, "curse")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        elif "xp from hunting and battling " in i:
                            try:
                                if autoHunt == False or autoBattle == False and doEvenIfDisabled:
                                    self.huntOrBattleSelected = False
                                    self.huntOrBattle = None
                                    if autoHunt == False and autoBattle == False:
                                        self.huntOrBattleSelected = False
                                        self.huntOrBattle = "hunt"
                                        self.hb = 0
                                        self.huntQuestValue = None
                                        self.battleQuestValue = None
                                        self.send_hunt_or_battle.start()
                                    elif autoHunt or autoBattle:
                                        self.huntOrBattleSelected = False
                                        self.huntOrBattle = "hunt"
                                        self.hb = 0
                                        self.huntQuestValue = None
                                        self.battleQuestValue = None
                                    print("enabled Earn xp quest", self.user)
                            except Exception as e:
                                print(e, "xp")
                                #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                        try:
                            #print(self.questsList)
                            if self.questsListInt != None:
                                questsList.pop(self.questsListInt)
                            questsList.append([self.user.id, self.channel_id, self.cm.guild.id, self.questsList])
                            for i in range(token_len):
                                if questsList[i][0] == self.user.id:
                                    self.questsListInt = i
                                    break
                            #else:
                                #quesstList[self.questsListInt] = [self.user.id, self.channel_id, self.cm.guild.id, self.questsList]
                            self.questsList = []
                            #print(questsList)
                        except Exception as e:
                            print(e, "last part of quest logs")
                            #run_system_command(f"termux-toast -c green -b black 'bug Detected:- {self.user.name}'", timeout=5, retry=True)
                    if giveawayEnabled and embed.author.name is not None and " A New Giveaway Appeared!" in embed.author.name and message.channel.id in giveawayChannels:
                        try:
                            await asyncio.sleep(random.uniform(gawMinCd,gawMaxCd))
                            await message.components[0].children[0].click()
                            console.print(f"-{self.user}[+] Joined giveaway in {message.channel.name} successfuly!".center(console_width - 2 ), style = "medium_purple3 on black")
                        except Exception as e:
                            console.print(f"-{self.user}[!] Error:- Giveaway,, {e}".center(console_width - 2 ), style = "medium_purple3 on black")
#----------ON MESSAGE EDIT----------#
    async def on_message_edit(self, before, after):
        if before.author.id != 408785106942164992:
            return
        if before.channel.id != self.channel_id:
            return
        if autoSlots != True and autoCf != True:
            return
        # slots
        if "slots" in after.content.lower():
            if "and won nothing... :c" in after.content:
              #  print(after.content)
                console.print(f"-{self.user}[+] ran Slots and lost {self.slotsLastAmt} cowoncy!.".center(console_width - 2 ), style = "magenta on black")
                if doubleOnLose:
                    self.slotsLastAmt = self.slotsLastAmt * 2
                self.gambleTotal-=self.slotsLastAmt
            else:
                #print(after.content)
                if "<:eggplant:417475705719226369>" in after.content.lower() and "and won" in after.content.lower():
                    console.print(f"-{self.user}[+] ran Slots and didn't win nor lose anything..".center(console_width - 2 ), style = "magenta on black")
                elif "and won" in after.content.lower():
                    self.gambleTotal+=self.slotsLastAmt
                    console.print(f"-{self.user}[+] ran Slots and won {self.slotsLastAmt}..".center(console_width - 2 ), style = "magenta on black")
                    if doubleOnLose:
                        self.slotsLastAmt = gambleStartValue
        #coinflip
        if "chose" in after.content.lower():
            try:
                if "and you lost it all... :c" in after.content.lower():
                    console.print(f"-{self.user}[+] ran Coinflip and lost {self.cfLastAmt} cowoncy!.".center(console_width - 2 ), style = "magenta on black")
                    self.gambleTotal-=self.cfLastAmt
                    if doubleOnLose:
                        print("cdble")
                        self.cfLastAmt = self.cfLastAmt*2
                        print(self.cfLastAmt)
                else:
                    console.print(f"-{self.user}[+] ran Coinflip and won {self.cfLastAmt} cowoncy!.".center(console_width - 2 ), style = "magenta on black")
                    self.gambleTotal+=self.cfLastAmt
                    if doubleOnLose:
                        print("c")
                        self.cfLastAmt = gambleStartValue
                        print(self.cfLastAmt)
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
    client = MyClient(token, channel_id)
    client.run(token, log_handler=None)
if __name__ == "__main__":
    console.print(owoPanel)
    print('-'*console_width)
    printBox(f'-Made by EchoQuill'.center(console_width - 2 ),'bold green on black' )
    printBox(f'-Current Version:- {version}'.center(console_width - 2 ),'bold cyan on black' )
    if websiteEnabled:
        printBox(f'-Website captcha logger:- http://localhost:{websitePort}/'.center(console_width - 2 ),'bold plum4 on black' )
    if int(ver_check.replace(".","")) > int(version.replace(".","")):
        console.print(f"""new update detected (v {ver_check}) (current version:- v {version})...
please update from -> https://github.com/EchoQuill/owo-dusk""", style = "yellow on black")
        if desktopNotificationEnabled:
            notification.notify(
                title = f'New Update!!, v{version_check}',
                message = "Update from v{version} to v{version_check} from our github page :>",
                app_icon = None,
                timeout = 15,
                )
    if autoPray == True and autoCurse == True:
        console.print("Both autoPray and autoCurse enabled. Only enable one!", style = "red on black")
        os._exit(0)
    if termuxNotificationEnabled and desktopNotificationEnabled:
        console.print("Only enable either termux notifs of desktop notifs.", style = "red on black")
        os._exit(0)
    tokens_and_channels = [line.strip().split() for line in open("tokens.txt", "r")]
    token_len = len(tokens_and_channels)
    printBox(f'-Recieved {token_len} tokens.'.center(console_width - 2 ),'bold magenta on black' )
    
    if desktopNotificationEnabled:
        notification.notify(
            title = f'{token_len} Tokens recieved!',
            message = "Thankyou for putting your trust on OwO-Dusk",
            app_icon = None,
            timeout = 15,
            )
    if termuxNotificationEnabled:
        run_system_command(f"termux-notification -c '{token_len} Tokens Recieved! Thanks for putting your trust on OwO-Dusk :>'", timeout=5, retry=True)
    if termuxToastEnabled:
        run_system_command(f"termux-toast -c magenta -b black 'owo-dusk started with {token_len} tokens!'", timeout=5, retry=True)
    #print(f"https://discord.com/api/webhooks/{webhookChannel}/{webhook_url.split('/')[-1]}")
    run_bots(tokens_and_channels)