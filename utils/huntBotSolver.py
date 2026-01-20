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


import numpy as np
import io
from PIL import Image
import base64

priority_groups = [
    list("abdegkmpqstvwxyz"),  # First priority
    list("fho"),  # Second priority
    list("cnru"),  # Third priority
    list("jl"),  # Fourth priority
    list("i"),  # Fifth priority
]

encoded_image_dict = {
    "a": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAARElEQVQoFWN0mv3/PwOJgIlE9WDlZGliJNYmZG+QZxOyCcTaSpZNZGliQXbSvlRGnAGD7A2ybGJENgHZVnxssmwiSxMARF4PhclsgWMAAAAASUVORK5CYII=",
    "b": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAYAAACAa1QyAAAAO0lEQVQoFWN0mv3/PwMU7EtlZISx8dFM+CRxyQ1yTYzIAYHLD+ji9PMTC7LV+OIJ2Rv0c95wtGmQpwgAPGAN2uSjSi0AAAAASUVORK5CYII=",
    "c": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAALklEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfF5ssm0Y1QYOTcXCnCADdtQb2r0ES3wAAAABJRU5ErkJggg==",
    "d": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAYAAACAa1QyAAAAOUlEQVQoFWNkIBI4zf7/H6aUCcYghR7kmhiRPUisv+jnJxZkJ+1LZWRE5iOzkb1BP+cNR5sGeYoAAJVGDLX7Igd2AAAAAElFTkSuQmCC",
    "e": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAP0lEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfmY3sDbJsYkQ2AdlkfGyybCJLE9EBgexcsmwa5AEBAB/ZDdI5nuFXAAAAAElFTkSuQmCC",
    "f": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAMUlEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfF5ssmxhHAwISnmSFHv00AQDzrwgdUIeJDgAAAABJRU5ErkJggg==",
    "g": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAR0lEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfF5tym2AmEwocsmwiSxNKQMCchy1AkJ1Mlk2MyCbAbCJEk2UTWZoA7Z4N1XlVX20AAAAASUVORK5CYII=",
    "h": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAYAAACAa1QyAAAAPUlEQVQoFWN0mv3/PwMU7EtlZISx8dFM+CRxyQ1yTYzIAYHLD+ji9PMTC7LV+OIJ2Rv0c96oTdD4oV9AAAB/TQsAYy1MLwAAAABJRU5ErkJggg==",
    "i": "iVBORw0KGgoAAAANSUhEUgAAAAkAAAANCAYAAAB7AEQGAAAAIklEQVQYGWNkQAJOs///h3H3pTIywthMMAY+elQRw2AMAgBW+wQa/q56owAAAABJRU5ErkJggg==",
    "j": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAN0lEQVQoFWNkIBI4zf7/H6aUCcYghR7VBA0tsgKCBTn896UyMhIT9GTZxIhsEzG2gNSQZRNZmgAmfgnRpvfItgAAAABJRU5ErkJggg==",
    "k": "iVBORw0KGgoAAAANSUhEUgAAAAwAAAANCAYAAACdKY9CAAAAaklEQVQoFYWR0Q3AIAhES0frLp2qu3Q1zSW95rhA8EeU94BoXM9ax7feO4Kx7+ROT1RnwsiNgsKj4DBGbjtUcNuhg0vBYUC60kgTDDEJWkljLVQKeA3/RErBgBU7kPnUwWFAfvcLnmBFlzY0ejHPkHfW8AAAAABJRU5ErkJggg==",
    "l": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAL0lEQVQoFWN0mv3/PwMU7EtlZISx8dFM+CRxyY1qgobMIA8IRuQUgSsy0cXp5ycAj5sG9B8JGsEAAAAASUVORK5CYII=",
    "m": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAMElEQVQoFWN0mv3/PwOJgIlE9WDllGval8rICMLItmMTo9wmZBvwsUdtgoYO/QICANPkB4nFxDDlAAAAAElFTkSuQmCC",
    "n": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAL0lEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfmY3sDbJsGtUEDc5BHhAAj7kG91sA1sEAAAAASUVORK5CYII=",
    "o": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAN0lEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfmY3sDbJsGtUEDU5G5KBEDmJ8bPqFHgBMzAnR80GexgAAAABJRU5ErkJggg==",
    "p": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAYAAACAa1QyAAAAQklEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfmY3sDbJsGtUEDU5G5KBEDmJ8bPqFHtEpAtm59HMe/WwCAJ8UCwJWTpYsAAAAAElFTkSuQmCC",
    "q": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAYAAACAa1QyAAAATUlEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfmY3sDbJsGtUEDU5G5KBEDmJ8bPqFHtYUgOxkbKmELOcRtAkWIMg2kmUTWZoAQwMR2VhDl78AAAAASUVORK5CYII=",
    "r": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAALUlEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfF5ssm0Y1QYNzkAcEACCxBBxWW3qwAAAAAElFTkSuQmCC",
    "s": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAANElEQVQoFWN0mv3/PwOJgIlE9WDlZGliQbZpXyojIzIfF5ssmxgHd0AQ5XFQgCB7YzgGBAAHzQyqIIdwIAAAAABJRU5ErkJggg==",
    "t": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAALUlEQVQoFWN0mv3/PwOJgIlE9WDlZGlixGYTspP3pTJiqCHLplFN0KAe5AEBAKu7BvTrMd81AAAAAElFTkSuQmCC",
    "u": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAMUlEQVQoFWN0mv3/PwMU7EtlZISx0WlkdUzoksTwRzVBQ2mQBwQjckwTE7EgNfTzEwDExgnPrPJ4NwAAAABJRU5ErkJggg==",
    "v": "iVBORw0KGgoAAAANSUhEUgAAAAwAAAANCAYAAACdKY9CAAAAd0lEQVQoFYWQAQ6AIAwDGfFl/sVX+Re+htSkpBssLDE09tqhpYy5397xQGdD3ygAtsdsF1CmKqCGvldds1ZCWgLWbQCkgGoW/IHTFsBkLib13DXTd38lA9mO0PINbMpOtwFQ3KLt8JcNEQCkswTUPIUnG681jSE+XwMvgvKD3yEAAAAASUVORK5CYII=",
    "w": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAALUlEQVQoFWN0mv3/PwMU7EtlZAQxCYkxwTSQQo9qgobWIA8IRuTYJzaC6ecnACGvDc/Z7HB/AAAAAElFTkSuQmCC",
    "x": "iVBORw0KGgoAAAANSUhEUgAAAAwAAAANCAYAAACdKY9CAAAAgklEQVQoFZWSiw2AIAxEi6PpKm6lqzgbesRnygVNJMGW3gcaG7XWmLfre8WvDacoiXsdaxTyHJc9Hs70BlDPZNUmd82EnGPQbnARoEfxihpljRzBMO0EAl0EEeH/plG6M3XFjLUbcgGiPwVO9+NGZIhgXQ8qurOf2/xoPJiVt3kCPwGLgnhJFhDySgAAAABJRU5ErkJggg==",
    "y": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAYAAACAa1QyAAAAPklEQVQoFWN0mv3/PwMU7EtlZISx0WlkdUzoksTwRzVBQ2mQBwQjckwTE7EgNfTzE9YEiuxkbImYfs6jn00ArlAN2LER5EoAAAAASUVORK5CYII=",
    "z": "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAT0lEQVQoFWN0mv3/PwOJgIlE9WDlZGliJGQTuvP3pTIy4tWETQPIEpyacGnAqQmfBqyaCGnA0ESMBhRNxGqAa0LXAJLABxhJ1QAyjKwUAQA6fySifLwVygAAAABJRU5ErkJggg==",
}


def decode_base64_to_image(b64_string):
    raw_bytes = base64.b64decode(b64_string)
    buffer = io.BytesIO(raw_bytes)
    return Image.open(buffer)


async def solveHbCaptcha(captcha_url, session):
    checks = []
    for item_list in priority_groups:
        for item in item_list:
            img = decode_base64_to_image(encoded_image_dict[item])
            checks.append((img, img.size, item))
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
