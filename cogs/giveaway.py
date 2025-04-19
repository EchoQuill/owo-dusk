# This file is part of owo-dusk.
#
# Copyright (c) 2024-present EchoQuill
#
# Portions of this file are based on code by EchoQuill, licensed under the
# GNU General Public License v3.0 (GPL-3.0).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import asyncio
import json
import discord

from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded



class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Join previous giveaways"""
    async def join_previous_giveaways(self):
        await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["shortCooldown"]))
        await self.bot.wait_until_ready()
        
        # Using briefcooldown here as using the long cooldown of giveaway joiner might look weird here.
        await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["briefCooldown"]))
        for i in self.bot.config_dict["giveawayJoiner"]["channelsToJoin"]:
            try:
                channel = await self.bot.fetch_channel(i)
            except discord.errors.NotFound:
                await self.bot.log(f"Giveaway channel {i} not found", "#ff5f00")
                continue
            except discord.errors.Forbidden:
                await self.bot.log(f"No permission to access giveaway channel {i}", "#ff5f00")
                continue
            except Exception as e:
                await self.bot.log(f"Error accessing giveaway channel {i}: {str(e)}", "#ff5f00")
                continue
                
            if not channel:
                # To prevent giving error if channel id is invalid
                await self.bot.log(f"Giveaway channel {i} seems to be invalid", "#ff5f00")
                continue
                
            await self.bot.set_stat(False)
            try:
                async for message in channel.history(limit=self.bot.config_dict["giveawayJoiner"]["messageRangeToCheck"]):
                    if message.embeds:
                        for embed in message.embeds:
                            if (embed.author and embed.author.name and 
                                " A New Giveaway Appeared!" in embed.author.name and 
                                message.channel.id in self.bot.config_dict["giveawayJoiner"]["channelsToJoin"]):
                                await asyncio.sleep(self.bot.random_float(self.bot.config_dict["defaultCooldowns"]["briefCooldown"]))
                                try:
                                    if (message.components and message.components[0].children and 
                                        message.components[0].children[0] and 
                                        not message.components[0].children[0].disabled):
                                        try:
                                            await message.components[0].children[0].click()
                                            await self.bot.log(f"{self.bot.user}[+] giveaway joined in {message.channel.name}", "#00d7af")
                                        except discord.errors.HTTPException as e:
                                            if e.code == 10004:  # Unknown Guild error
                                                await self.bot.log(f"Cannot join giveaway - guild is unavailable or deleted", "#ff5f00")
                                            elif e.code == 10062:  # Unknown Interaction error
                                                await self.bot.log(f"Cannot join giveaway - interaction expired", "#ff5f00")
                                            else:
                                                await self.bot.log(f"HTTP error when joining giveaway: {e}", "#ff5f00")
                                        except Exception as e:
                                            await self.bot.log(f"Error joining giveaway: {str(e)}", "#ff5f00")
                                except (IndexError, AttributeError):
                                    # Handle case where components might be malformed
                                    pass
            except Exception as e:
                await self.bot.log(f"Error checking history for channel {channel.id}: {str(e)}", "#ff5f00")

            await self.bot.set_stat(True)

    """gets executed when the cog is first loaded"""
    async def cog_load(self):
        if self.bot.config_dict["giveawayJoiner"]["enabled"]:
            """Run join_previous_giveaways when bot is ready"""
            asyncio.create_task(self.join_previous_giveaways())
        else:
            try:
                asyncio.create_task(self.bot.unload_cog("cogs.giveaway"))
            except ExtensionNotLoaded:
                pass
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Join Giveaways"""
        if message.channel.id in self.bot.config_dict["giveawayJoiner"]["channelsToJoin"]:
            if message.embeds:
                for embed in message.embeds:
                    if (embed.author and embed.author.name and 
                        " A New Giveaway Appeared!" in embed.author.name and 
                        message.channel.id in self.bot.config_dict["giveawayJoiner"]["channelsToJoin"]):
                        await asyncio.sleep(self.bot.random_float(self.bot.config_dict["giveawayJoiner"]["cooldown"]))
                        try:
                            if (message.components and message.components[0].children and 
                                message.components[0].children[0] and 
                                not message.components[0].children[0].disabled):
                                try:
                                    await message.components[0].children[0].click()
                                    await self.bot.log(f"{self.bot.user}[+] giveaway joined in {message.channel.name}", "#00d7af")
                                except discord.errors.HTTPException as e:
                                    if e.code == 10004:  # Unknown Guild error
                                        await self.bot.log(f"Cannot join giveaway - guild is unavailable or deleted", "#ff5f00")
                                    elif e.code == 10062:  # Unknown Interaction error
                                        await self.bot.log(f"Cannot join giveaway - interaction expired", "#ff5f00")
                                    else:
                                        await self.bot.log(f"HTTP error when joining giveaway: {e}", "#ff5f00")
                        except (IndexError, AttributeError):
                            # Handle case where components might be malformed
                            pass

async def setup(bot):
    await bot.add_cog(Giveaway(bot))