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


class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log(f"conf2 - lottery","purple")
    
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
                print(self.bot.calc_time())
                await asyncio.sleep(self.bot.calc_time())  # Wait until next 12:00 AM PST

            await asyncio.sleep(self.bot.random_float(config_dict["defaultCooldowns"]["briefCooldown"]))
            #self.bot.queue.put(["lottery", f" {config_dict["commands"]["lottery"]["amount"]}"])
            self.bot.put_queue(f"lottery {config_dict['commands']['lottery']['amount']}")
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
                        self.bot.remove_queue("lottery")
                        print(self.bot.calc_time())
                        await asyncio.sleep(self.bot.calc_time())
                        await asyncio.sleep(self.random_float(config_dict["defaultCooldowns"]["moderateCooldown"]))
                        self.bot.put_queue(f"lottery {config_dict['commands']['lottery']['amount']}")
                        self.bot.log("put to queue - Lottery", "honeydew2")
                        with lock:
                            accounts_dict[str(self.bot.user.id)]["lottery"] = self.time_in_seconds()
                            with open("utils/stats.json", "w") as f:
                                json.dump(accounts_dict, f, indent=4)
                
async def setup(bot):
    await bot.add_cog(Lottery(bot))