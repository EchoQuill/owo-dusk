import os
import discord
import json
import time
import threading

#desktop
from plyer import notification
from playsound3 import playsound

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)

"""
To check if the code is running with Termux or not
"""
def is_termux():
    termux_prefix = os.environ.get("PREFIX")
    termux_home = os.environ.get("HOME")
    
    if termux_prefix and "com.termux" in termux_prefix:
        return True
    elif termux_home and "com.termux" in termux_home:
        return True
    else:
        return os.path.isdir("/data/data/com.termux")
    
def run_system_command(command, timeout, retry=False, delay=5):
    def target():
        try:
            os.system(command)
        except Exception as e:
            print(f"Error executing command: {command} - {e}")

    # Create and start a thread to execute the command
    thread = threading.Thread(target=target)
    thread.start()

    # Wait for the thread to finish, with a timeout
    thread.join(timeout)

    # If the thread is still alive after the timeout, terminate it
    if thread.is_alive():
        print(f"-error[0] {command} command failed!")
        if retry:
            print(f"-system[0] Retrying '{command}' after {delay}s")
            time.sleep(delay)
            run_system_command(command, timeout, retry=False)
    
def get_channel_name(channel):
    if isinstance(channel, discord.DMChannel):
        return "owo DMs"
    return channel.name

def captcha_handler(channel, username, captcha_type):
    mobile = is_termux()
    channel_name = get_channel_name(channel)
    """Notifications"""
    if config_dict["captcha"]["notifications"]["enabled"]:
        try:
            if mobile:
                run_system_command(f"termux-notification -c '{config_dict["captcha"]["notifications"]["captchaContent"].format(username=username,channelname=channel_name,captchatype=captcha_type)}'", timeout=5, retry=True)
            else:
                notification.notify(
                    title=f'{username} DETECTED CAPTCHA',
                    message=config_dict["captcha"]["notifications"]["captchaContent"].format(username=username,channelname=channel_name,captchatype=captcha_type),
                    app_icon=None,
                    timeout=15
                    )
        except Exception as e:
            print(f"{e} - at notifs")
    """Play audio file"""
    """
    TASK: add two checks, check the path for the file in both outside utils folder
    and in owo-dusk folder
    +
    better error handling for missing PATH
    """
    if config_dict["captcha"]["playAudio"]["enabled"]:
        try:
            if mobile:
                run_system_command(f"termux-media-player play {config_dict["playAudio"]["path"]}", timeout=5, retry=True)
            else:
                playsound(config_dict["playAudio"]["path"], block=False)
        except Exception as e:
            print(f"{e} - at audio")
    """Toast/Popup"""
    if config_dict["captcha"]["toastOrPopup"]["enabled"]:
        try:
            if mobile:
                run_system_command(f"termux-toast -c {config_dict["captcha"]["toastOrPopup"]["termuxToast"]["textColour"]} -b {config_dict["captcha"]["toastOrPopup"]["termuxToast"]["backgroundColour"]} '{config_dict["captcha"]["toastOrPopup"]["captchaContent"].format(username=username,channelname=channel_name,captchatype=captcha_type)}'", timeout=5, retry=True)
            else:
                pass
        except Exception as e:
            print(f"{e} - at Toast/Popup")



    



