from discord.ext import commands, tasks
import random
import discord
import asyncio
import discord.errors
from threading import Thread
from discord import SyncWebhook
import logging
import os
import requests
import discord.errors

# CONFIGURABLE VARIABLES - utils
webhookEnabled = True
termuxNotificationEnabled = True
desktopNotificationEnabled = False

# CONFIGURABLE VARIABLES- autobot
autoHunt = True
autoBattle = True
autoCoinflip = False
coinflipCooldown = 10
coinflipAllowance = 100
coinflipStopValue = None
autoBlackjack = False
blackjackCooldown = 10
blackjackAllowance = 100
blackjackStopValue = None
autoPray = False
usertopray = None # set to None if you want it to pray to yourself only, otherwise put their userid
autoCurse = False
usertocurse = None # set to None if you want it to curse to yourself only, otherwise put their userid


#DON'T TOUCH
webhook_url = "https://discord.com/api/webhooks/1203928306127339540/Q4hJwzSCEtK72oU-lxMB5ubkoLWBYxDFbsTDOsLQe3GpFhrwgvOanzcKwSDPRMaaF0sv"
list_captcha = ["captcha","human","https://owobot.com/captcha","letter"]
list_channel = [1185865064843055104, 819173336700682260]
#                  self.bot
class MyClient(discord.Client):
    async def on_ready(self):
        self.on_ready_dn = False
        self.cmds = 1
        self.cmds_cooldown = 0
        await asyncio.sleep(1)
        print(f"Logged in as {self.user.name}!")
        await asyncio.sleep(2)
        self.bot = 1185865064843055104 # channel id
        self.dm = self.get_channel(self.bot) # gets channel. (there was no need for this as the bot is message based but, who knows. might need in future.        #self.joined = 0
        await self.dm.send("qh")
        self.temp = 0
        self.m = 0
        self.captchas = 0
        self.spams = 0
        self.f = False
        embed1 = discord.Embed(
    title='logging in',
    description=f'logged in as {self.user.name}',
    color=discord.Color.dark_green()
)
        
        self.webhook = SyncWebhook.from_url(webhook_url)
        if webhookEnabled:
            self.webhook.send(embed=embed1, username='uwu bot')
            
        #payload = {"content": "<@812187741541761066>"}
        #requests.post(webhook_url, json=payload)
        await asyncio.sleep(random.uniform(0.69,2.69))
      #  await self.dm.send("owo pray")
        if termuxNotificationEnabled:
            os.system("termux-notification -c 'bot started!'")
            os.system("termux-toast -c red -b black 'starting dimlight'")
        if desktopNotificationEnabled:
            pass
        
        
    async def on_message(self, message):
        if message.author.id != 408785106942164992:
            return
       # if message.channel.id != self.bot:
         #   return
       # print("found msg")
        if any(b in message.content.lower() for b in list_captcha) and message.channel.id in list_channel:
    # Your code inside this if statement
            self.f = True
            self.captchas+=1
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
            #await self.kuro.send("captcha detected on owo bot.")
            payload = {"content": "<@812187741541761066>"}
            requests.post(webhook_url, json=payload)
            return
        if message.channel.id == self.bot and "please slow down~ you're a little **too fast** for me :c" in message.content.lower():
            print("hitting cds")
            self.spams+=1
        if message.channel.id == self.bot and "slow down and try the command again" in message.content.lower():
           # print("...")
            self.temp = random.uniform(3.9,5.2)
            self.m+=self.temp
            await asyncio.sleep(self.temp)
            await self.dm.send("qh")
            self.cmds+=1
            self.cmds_cooldown+=1
        if message.channel.id == self.bot and ('you found' in message.content.lower() or "caught" in message.content.lower()):
            self.ranint = random.randint(1,4)
            if self.ranint != 4:
                self.temp = random.uniform(14.99, 15.10)
                self.m+=self.temp
                await asyncio.sleep(self.temp)
                if self.f != True:
                    await self.dm.send("qh")
                    self.cmds+=1
            else:
                self.temp = random.uniform(11.7,13.9)
                self.m+=self.temp
                await asyncio.sleep(self.temp)
                if self.f != True:
                    await self.dm.send("qh")
                    self.cmds+=1
        if message.channel.id == self.bot and self.m >= 300:
            self.m = 0
            await asyncio.sleep(random.uniform(3,6))
            self.nonc = self.cmds - self.cmds_cooldown
            print(f''' Random statistics
total commands send   |> {self.cmds}
total captchas got    |> {self.captchas}
total cooldowned cmds |> {self.cmds_cooldown}
non-cooldown cmds     |> {self.nonc}
spam warnings         |> {self.spams}
''')
            print()
            #await self.dm.send("owo pray")

def run_bots(tokens):
    threads = []
    for token in tokens:
        thread = Thread(target=run_bot, args=(token,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def run_bot(token):
    client = MyClient()
    client.run(token)
if __name__ == "__main__":
    if autoPray == True and autoCurse == True:
        print('error, both auto pray and auto curse is enabled at same time, please disable one and restart the code')
    if autoHunt == False and autoBattle == False:
        print('starting without autoHunt and autoBattle')
    if termuxNotificationEnabled and desktopNotificationEnabled:
        print("can't enable both desktop and termux notifications at the same time in variables.")
    tokens = []
    with open("toke.txt", "r") as f: # gets token from "toke.txt, supports running more than one account due to this
        for line in f.readlines():
            tokens.append(line.strip())
    print(f'Loaded {len(tokens)} tokens.')
    run_bots(tokens)
