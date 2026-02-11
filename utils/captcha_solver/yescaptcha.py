from curl_cffi.requests import AsyncSession
from curl_cffi import requests
import asyncio
import json


class captchaClient:
    def __init__(self, api):
        self.api = api
        self.balance = self.get_yescaptcha_balance() or 0
        self._site_key = "a6a1d5ce-612d-472d-8e37-7601408fbc09"
        self._payload = {
            "authorize": True,
            "integration_type": 0,
            "permissions": "0",
            "location_context": {
                "guild_id": "10000",
                "channel_id": "10000",
                "channel_type": 10000,
            },
        }
        self._auth_url = r"https://discord.com/api/v9/oauth2/authorize?client_id=408785106942164992&response_type=code&redirect_uri=https://owobot.com/api/auth/discord/redirect&scope=identify guilds"

    def get_yescaptcha_balance(self):
        url = "https://api.yescaptcha.com/getBalance"
        try:
            response = requests.post(url, json={"clientKey": self.api}, timeout=10)
            data = response.json()
            return int(data.get("balance", 0)) if data.get("errorId") == 0 else 0
        except Exception:
            return 0

    def update_balance(self):
        self.balance = self.get_yescaptcha_balance()

    async def solve_hcaptcha_logic(self):
        """Use Yescaptcha api to solve captcha"""
        create_url = "https://api.yescaptcha.com/createTask"
        payload = {
            "clientKey": self.api,
            "task": {
                "type": "HCaptchaTaskProxyless",
                "websiteKey": self._site_key,
                "websiteURL": "https://owobot.com",
            },
            "softID": 94493,
        }

        async with AsyncSession() as session:
            resp = await session.post(create_url, json=payload)
            data = resp.json()
            if data.get("errorId") != 0:
                raise Exception(data.get("errorDescription"))

            task_id = data.get("taskId")
            while True:
                await asyncio.sleep(3)
                result_resp = await session.post(
                    "https://api.yescaptcha.com/getTaskResult",
                    json={"clientKey": self.api, "taskId": task_id},
                )
                res = result_resp.json()
                if res.get("status") == "ready":
                    return res["solution"]["gRecaptchaResponse"]
                if res.get("errorId") != 0:
                    raise Exception(res.get("errorDescription"))

    async def solve_owo_bot_captcha(self, discord_headers):
        discord_headers["Referer"] = self._auth_url
        self.update_balance()
        itr = 0
        if self.balance < 30:
            while itr != 3:
                print("Not enough balance to solve captcha")
                itr+=1
                if self.balance < 30:
                    break
                await asyncio.sleep(0.5)
            if self.balance < 30:
                return False


        async with AsyncSession(impersonate="chrome120") as session:
            # Authorize via Discord
            oauth_resp = await session.post(
                self._auth_url,
                json=self._payload,
                headers=discord_headers,
                allow_redirects=True,
            )

            await session.get(json.loads(oauth_resp.text).get("location"))

            await session.get("https://owobot.com/captcha")

            # 3. Verify Session is active
            auth_resp = await session.get("https://owobot.com/api/auth")
            auth_data = auth_resp.json()
            print(auth_data)

            if not auth_data or auth_data.get("banned"):
                print("Auth Failed or Account Banned.")
                return False

            if not auth_data.get("captcha", {}).get("active"):
                print("No active captcha?")
                return False

            try:
                solution = await self.solve_hcaptcha_logic()
            except Exception as e:
                print(f"Solver Error: {e}")
                return False

            verify_resp = await session.post(
                "https://owobot.com/api/captcha/verify",
                json={"token": solution},
                headers={
                    "Referer": "https://owobot.com/captcha",
                    "Origin": "https://owobot.com",
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json",
                },
            )

            if verify_resp.status_code == 200:
                print("Verification successful!")
                self.update_balance()
                return True
            else:
                print(f"Verification failed (Status {verify_resp.status_code})")
                print(f"Server Response: {verify_resp.text}")
                return False
