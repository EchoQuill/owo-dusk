# This file includes code originally authored by realphandat.
# Source: "phandat-selfbot" (https://github.com/realphandat/phandat-selfbot)
# This file is licensed under the GNU General Public License v3.0 (GPL-3.0).
# 
# This project as a whole is also licensed under the GNU General Public License v3.0.

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


import glob
import os
import numpy as np
import aiohttp
import io
from PIL import Image
import requests

"""
Made with the help of https://github.com/realphandat/phandat-selfbot/blob/main/owo/modules.py
I have recieved permission to use this code snippet.
"""


async def solveHbCaptcha(captcha_url, session):
    checks = []
    """
    I tried my best to make these work without folder seperation but uhh failed lol.
     ill think of a way later but hey, it works somehow with folder seperation
    """ 
    check_images = glob.glob("static/imgs/corpus/**/*.png")
    for check_image in sorted(check_images):
        img = Image.open(check_image)
        checks.append((img, img.size, os.path.basename(check_image).split(".")[0]))
    """
    the above is basically the size, img and path (name to be used if matched)
    """
    try:
        # get img, aiohttp session passed from main file
        # iam not making the mistake of making session each time lol.
        async with session.get(captcha_url) as resp:
            if resp.status == 200 and "image" in resp.headers.get("Content-Type", ""):
                large_image = Image.open(io.BytesIO(await resp.read()))
                large_array = np.array(large_image)
            else:
                print("Failed to fetch a valid image.")
                return ""

    except Exception as e:
        print(f"Error fetching the captcha image: {e}")
        return ""
    matches = []
    for img, (small_w, small_h), letter in checks:
        small_array = np.array(img)
        """
        This mask part makes sure transparent part are not compared.
        with this the captcha can be easily solved.
        """
        mask = small_array[:, :, 3] > 0  # Alpha mask for non-transparent pixels

        for y in range(large_array.shape[0] - small_h + 1):
            for x in range(large_array.shape[1] - small_w + 1):
                segment = large_array[y : y + small_h, x : x + small_w]
                if np.array_equal(segment[mask], small_array[mask]):
                    """
                    prevents matching of letters close with prev matched letters
                    """
                    if not any(
                        (m[0] - small_w < x < m[0] + small_w)
                        and (m[1] - small_h < y < m[1] + small_h)
                        for m in matches
                    ):
                        matches.append(
                            (x, y, letter)
                        )  # no need of x,y here but ill let it stay
    matches = sorted(matches, key=lambda tup: tup[0])
    return "".join([i[2] for i in matches])
