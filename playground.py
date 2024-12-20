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

import time
from datetime import timedelta

# Example Discord timestamp
discord_timestamp = 1731820039

# Current Unix timestamp
current_timestamp = int(time.time())

# Time difference
remaining_seconds = discord_timestamp - current_timestamp

if remaining_seconds > 0:
    # Convert to human-readable format
    time_left = str(timedelta(seconds=remaining_seconds))
    print(f"Time left: {time_left}")
else:
    print("The timestamp has already passed.")
