import json
import pytz
import asyncio
import threading

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded
from datetime import datetime, timezone

def load_json_dict(file_path="utils/stats.json"):
    with open(file_path, "r") as config_file:
        return json.load(config_file)

lock = threading.Lock()
accounts_dict = load_json_dict()
config_dict = load_json_dict("config.json")


class Cookie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - cookie","purple")
    
    """change to conver times"""
    def time_in_seconds(self, time_to_convert=None):
        if time_to_convert is None:
            time_to_convert = datetime.now(timezone.utc).astimezone(pytz.timezone('US/Pacific'))
        return time_to_convert.timestamp()

    async def start_cookie(self):
        if str(self.bot.user.id) in accounts_dict:
            self.bot.log("cookie - 0", "honeydew2")
            self.current_time_seconds = self.time_in_seconds()
            self.last_cookie_time = accounts_dict[str(self.bot.user.id)].get("cookie", 0)

            # Time difference calculation
            self.time_diff = self.current_time_seconds - self.last_cookie_time
            print(self.current_time_seconds, self.last_cookie_time)
            print(self.time_diff, "time diff")

            if self.time_diff < 0:
                self.last_cookie_time = self.current_time_seconds
            if self.time_diff < 86400:  # 86400 = seconds till a day(24hrs).
                print(self.bot.calc_time())
                await asyncio.sleep(self.bot.calc_time())  # Wait until next 12:00 AM PST

            await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["briefCooldown"]))
            if config_dict["commands"]["cookie"]["pingUser"]:
                self.bot.put_queue(f"cookie <@{config_dict['commands']['cookie']['userid']}>")
                #self.bot.queue.put(["cookie ", f" <@{config_dict["commands"]["cookie"]["userid"]}>"])
            else:
                self.bot.put_queue(f"cookie {config_dict['commands']['cookie']['userid']}")
            self.bot.log("put to queue - lottry", "honeydew2")

            with lock:
                accounts_dict[str(self.bot.user.id)]["cookie"] = self.time_in_seconds()
                with open("utils/stats.json", "w") as f:
                    json.dump(accounts_dict, f, indent=4)

    async def cog_load(self):
        self.bot.log(f"cookie - start", "purple")
        if not config_dict["commands"]["cookie"]["enabled"]:
            try:
                await self.bot.unload_extension("cogs.cookie")
            except ExtensionNotLoaded:
                pass
        else:
            asyncio.create_task(self.start_cookie())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.cm.id and message.author.id == self.bot.owo_bot_id:
            if "You got a cookie from" in message.content:
                self.bot.remove_queue("cookie")
                print(self.bot.calc_time())
                await asyncio.sleep(self.bot.calc_time())
                await asyncio.sleep(self.random_float(config_dict["defaultCooldowns"]["moderateCooldown"]))
                if config_dict["commands"]["cookie"]["pingUser"]:
                    self.bot.put_queue(f"cookie <@{config_dict['commands']['cookie']['userid']}>")
                else:
                    self.bot.put_queue(f"cookie {config_dict['commands']['cookie']['userid']}")
                self.bot.log("put to queue - cookie", "honeydew2")
                with lock:
                    accounts_dict[str(self.bot.user.id)]["cookie"] = self.time_in_seconds()
                    with open("utils/stats.json", "w") as f:
                        json.dump(accounts_dict, f, indent=4)
                
async def setup(bot):
    await bot.add_cog(Cookie(bot))