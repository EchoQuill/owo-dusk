import json
import asyncio
import pytz
import threading

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded
from datetime import datetime, timedelta, timezone

def load_json_dict(file_path="utils/stats.json"):
    with open(file_path, "r") as config_file:
        return json.load(config_file)

lock = threading.Lock()
accounts_dict = load_json_dict()
config_dict = load_json_dict("config.json")


class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - lottery","purple")

    def calc_time(self):
        pst_timezone = pytz.timezone('US/Pacific') #gets timezone
        current_time_pst = datetime.now(timezone.utc).astimezone(pst_timezone) #current pst time
        midnight_pst = pst_timezone.localize(datetime(current_time_pst.year, current_time_pst.month, current_time_pst.day, 0, 0, 0)) #gets 00:00 of the day
        time_until_12am_pst = midnight_pst + timedelta(days=1) - current_time_pst # adds a day to the midnight to get time till next midnight, then subract it with current time
        total_seconds = time_until_12am_pst.total_seconds() # turn that time to seconds
        # 12am = 00:00, I might need this the next time I take a look here.
        return total_seconds
    
    """change to conver times"""
    def time_in_seconds(self, time_to_convert=None):
        if time_to_convert is None:
            time_to_convert = datetime.now(timezone.utc).astimezone(pytz.timezone('US/Pacific'))
        return time_to_convert.timestamp()

    async def start_lottery(self):
        if str(self.bot.user.id) in accounts_dict:
            self.bot.log("lottery - 0", "honeydew2")
            self.current_time_seconds = self.time_in_seconds()
            self.last_lottery_time = accounts_dict[str(self.bot.user.id)].get("lottery", 0)

            # Time difference calculation
            self.time_diff = self.current_time_seconds - self.last_lottery_time
            print(self.current_time_seconds, self.last_lottery_time)
            print(self.time_diff, "time diff")

            if self.time_diff < 0:
                self.last_lottery_time = self.current_time_seconds
            if self.time_diff < 86400:  # 86400 = seconds till a day(24hrs).
                print(self.calc_time())
                await asyncio.sleep(self.calc_time())  # Wait until next 12:00 AM PST

            await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["briefCooldown"]))
            self.bot.queue.put(["lottery", f" {config_dict["commands"]["lottery"]["amount"]}"])
            self.bot.log("put to queue - lottry", "honeydew2")

            with lock:
                accounts_dict[str(self.bot.user.id)]["lottery"] = self.time_in_seconds()
                with open("utils/stats.json", "w") as f:
                    json.dump(accounts_dict, f, indent=4)

    async def cog_load(self):
        self.bot.log(f"lottery - start", "purple")
        if not config_dict["commands"]["lottery"]["enabled"]:
            try:
                await self.bot.unload_extension("cogs.lottery")
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_lottery())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if message.embeds:
                for embed in message.embeds:
                    if embed.author.name is not None and "'s Lottery Submission" in embed.author.name:
                        self.bot.checks = [check for check in self.bot.checks if check[0] != "lottery"]
                        print(self.calc_time())
                        await asyncio.sleep(self.calc_time())
                        await asyncio.sleep(self.random_float(config_dict["defaultCooldowns"]["moderateCooldown"]))
                        self.bot.queue.put(["lottery", f" {config_dict["commands"]["lottery"]["amount"]}"])
                        self.bot.log("put to queue - Lottery", "honeydew2")
                        with lock:
                            accounts_dict[str(self.bot.user.id)]["lottery"] = self.time_in_seconds()
                            with open("utils/stats.json", "w") as f:
                                json.dump(accounts_dict, f, indent=4)
                
async def setup(bot):
    await bot.add_cog(Lottery(bot))