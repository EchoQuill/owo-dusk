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

import json
import base64
import uuid
import re
from datetime import datetime
import aiohttp


async def extract_asset_files(session: aiohttp.ClientSession, headers):
    async with session.get("https://discord.com/login", headers=headers) as resp:
        text = await resp.text()

    pattern = r'<script\s+src="([^"]+\.js)"\s+defer>\s*</script>'
    return re.findall(pattern, text)


_SENTRY_ASSET_REGEX = re.compile(r"assets/(sentry\.\w+)\.js")
_BUILD_NUMBER_REGEX = re.compile(r'buildNumber\D+(\d+)"')


async def get_build_number(session: aiohttp.ClientSession) -> int:
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://discord.com/login",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    }

    try:
        async with session.get("https://discord.com/login", headers=headers) as resp:
            app_html = await resp.text()

        match = _SENTRY_ASSET_REGEX.search(app_html)
        if not match:
            raise RuntimeError("Could not find sentry asset file")

        sentry = match.group(1)
        sentry_url = f"https://static.discord.com/assets/{sentry}.js"

        async with session.get(sentry_url, headers=headers) as resp:
            js_content = await resp.text()

        match = _BUILD_NUMBER_REGEX.search(js_content)
        if not match:
            raise RuntimeError("Could not find build number")

        return int(match.group(1))

    except Exception:
        return 307749


async def get_browser_version(session: aiohttp.ClientSession) -> int:
    url = "https://versionhistory.googleapis.com/v1/chrome/platforms/win/channels/stable/versions"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            data = await resp.json()
        return int(data["versions"][0]["version"].split(".")[0])
    except Exception:
        return 134


def generate_properties(build_number: int, browser_version: int) -> dict:
    # loc = locale.getdefaultlocale()[0] or "en-US"

    return {
        "os": "Windows",
        "browser": "Chrome",
        "device": "",
        "system_locale": "en-US",  # loc.replace("_", "-"),
        "browser_user_agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{browser_version}.0.0.0 Safari/537.36",
        "browser_version": f"{browser_version}.0.0.0",
        "os_version": "10",
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": build_number,
        "client_event_source": None,
        "has_client_mods": False,
        "client_launch_id": str(uuid.uuid4()),
        "client_app_state": "unfocused",
        "client_heartbeat_session_id": str(uuid.uuid4()),
    }


def generate_x_super(props: dict) -> str:
    json_str = json.dumps(props, separators=(",", ":"))
    return base64.b64encode(json_str.encode("utf-8")).decode("utf-8")


async def generate_headers() -> dict:
    timeout = aiohttp.ClientTimeout(total=15)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        props = None
        encoded = None

        try:
            async with session.post(
                "https://cordapi.dolfi.es/api/v2/properties/web"
            ) as resp:
                data = await resp.json()
                props = data.get("properties")
                encoded = data.get("encoded")
        except Exception:
            pass

        if not props:
            print("dolfies failed...\n")
            bv = await get_browser_version(session)
            bn = await get_build_number(session)
            props = generate_properties(bn, bv)
            encoded = generate_x_super(props)

        tzname = datetime.now().astimezone().tzname() or "UTC"

        return {
            "accept": "*/*",
            "accept-language": f"{props.get('system_locale', 'en-US')},en;q=0.5",
            # "priority": "u=1, i",
            # "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": f'"Not:A-Brand";v="24", "Chromium";v="{props.get("browser_version", "124")}"',
            "sec-ch-ua-platform": f'"{props.get("os", "Windows")}"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-discord-locale": props.get("system_locale", "en-US"),
            "x-discord-timezone": tzname,
            "x-super-properties": encoded,
            "origin": "https://discord.com",
            "x-debug-options": "bugReporterEnabled",
            "User-Agent": props.get("browser_user_agent", "Mozilla/5.0"),
            "Host": "discord.com",
            "Content-Type": "application/json",
            "Authorization": "",
            "Connection": "keep-alive",
            "Sec-GPC": "1",
            "Priority": "u=0",
            "TE": "trailers",
        }


if __name__ == "__main__":
    import asyncio

    headers = asyncio.run(generate_headers())
    print(headers)
