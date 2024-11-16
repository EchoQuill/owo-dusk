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


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - daily","purple")

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
    
    async def start_daily(self):
        if str(self.bot.user.id) in accounts_dict:
            self.bot.log("daily - 0", "honeydew2")
            self.current_time_seconds = self.time_in_seconds()
            self.last_daily_time = accounts_dict[str(self.bot.user.id)].get("daily", 0)

            # Time difference calculation
            self.time_diff = self.current_time_seconds - self.last_daily_time
            print(self.current_time_seconds, self.last_daily_time)
            print(self.time_diff, "time diff")

            if self.time_diff < 0:
                self.last_daily_time = self.current_time_seconds
            if self.time_diff < 86400:  # 86400 = seconds till a day(24hrs).
                print(self.calc_time())
                await asyncio.sleep(self.calc_time())  # Wait until next 12:00 AM PST

            await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["briefCooldown"]))
            self.bot.queue.put("daily")
            self.bot.log("put to queue - Daily", "honeydew2")

            with lock:
                accounts_dict[str(self.bot.user.id)]["daily"] = self.time_in_seconds()
                with open("utils/stats.json", "w") as f:
                    json.dump(accounts_dict, f, indent=4)

    async def cog_load(self):
        self.bot.log(f"daily - start", "purple")
        if not config_dict["autoDaily"]:
            try:
                await self.bot.unload_extension("cogs.daily")
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_daily())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if "Here is your daily **<:cowoncy:416043450337853441>" in message.content:
                """Task: add cash check regex here"""
                self.bot.checks = [check for check in self.bot.checks if check[0] != "daily"]
                print(self.calc_time())
                await asyncio.sleep(self.calc_time())
                await asyncio.sleep(self.random_float(config_dict["defaultCooldowns"]["moderateCooldown"]))
                self.bot.queue.put("daily")
                self.bot.log("put to queue - Daily", "honeydew2")
                with lock:
                    accounts_dict[str(self.bot.user.id)]["daily"] = self.time_in_seconds()
                    with open("utils/stats.json", "w") as f:
                        json.dump(accounts_dict, f, indent=4)

            if "**⏱ |** Nu! **" in message.content and "! You need to wait" in message.content:
                self.bot.log("Nu - Daily", "honeydew2")
                self.bot.checks = [check for check in self.bot.checks if check[0] != "daily"]
                print(self.calc_time())
                await asyncio.sleep(self.calc_time())
                await asyncio.sleep(self.random_float(config_dict["defaultCooldowns"]["moderateCooldown"]))
                self.bot.queue.put("daily")
                self.bot.log("put to queue - Daily", "honeydew2")
                with lock:
                    accounts_dict[str(self.bot.user.id)]["daily"] = self.time_in_seconds()
                    with open("utils/stats.json", "w") as f:
                        json.dump(accounts_dict, f, indent=4)
                
async def setup(bot):
    await bot.add_cog(Daily(bot))