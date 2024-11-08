import json

from discord.ext import commands

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

list_captcha = ["to check that you are a human!","https://owobot.com/captcha","please reply with the following", "captcha"]

class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log("conf2 - OwO","purple")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if "I have verified that you are human! Thank you! :3" in message.content:
                self.bot.captcha = False
                self.bot.log(f"captcha solved! - {self.bot.user}", "chartreuse3")

        if message.channel.id == self.bot.dm.id and message.author.id == self.bot.owo_bot_id:
            if any(b in message.content.lower() for b in list_captcha):
                self.bot.captcha = True
                self.bot.log(f"captcha detected! - {self.bot.user}", "indian_red")
                

                
                


async def setup(bot):
    await bot.add_cog(Captcha(bot))