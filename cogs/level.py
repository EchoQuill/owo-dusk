import asyncio
import string
import random
import json

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

def generate_random_string():
    """something like a list?"""
    characters = string.ascii_lowercase + ' '
    length = random.randint(config_dict["commands"]["lvlGrind"]["minLengthForRandomString"], config_dict["commands"]["lvlGrind"]["maxLengthForRandomString"])
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - OwO","purple")
        self.last_level_grind_message = None

    async def start_level_grind(self):
        try:
            await asyncio.sleep(self.bot.random_float(config_dict["commands"]["lvlGrind"]["cooldown"]))
            self.last_level_grind_message = generate_random_string()
            self.bot.put_queue(self.last_level_grind_message, prefix=False)
        except Exception as e:
            print(e)
        
    
    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if not config_dict["commands"]["lvlGrind"]["enabled"]:
            try:
                self.bot.log("test", "purple")
                await self.bot.unload_extension("cogs.level")
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_level_grind())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.user.id:
            if self.last_level_grind_message == message.content:
                self.bot.log(f"lvlgrind msg detected from {message.author.name}.","cornflower_blue")
                self.start_level_grind()
                

async def setup(bot):
    await bot.add_cog(Level(bot))