"""
Platform-specific utilities for owo-dusk.
Provides cross-platform compatibility functions for various operating systems.
"""

import os
import sys
import platform
import subprocess
import threading
import time
from pathlib import Path

def is_termux():
    """Check if the code is running in Termux environment."""
    termux_prefix = os.environ.get("PREFIX")
    termux_home = os.environ.get("HOME")
    
    if termux_prefix and "com.termux" in termux_prefix:
        return True
    elif termux_home and "com.termux" in termux_home:
        return True
    else:
        return os.path.isdir("/data/data/com.termux")

# Determine OS type
PLATFORM = platform.system().lower()
IS_WINDOWS = PLATFORM == "windows"
IS_MACOS = PLATFORM == "darwin"
IS_LINUX = PLATFORM == "linux"
IS_TERMUX = is_termux()

def clear_screen():
    """Clear the terminal screen in a cross-platform way."""
    if IS_WINDOWS:
        os.system('cls')
    else:
        os.system('clear')

def normalize_path(path):
    """Normalize file paths for cross-platform compatibility."""
    return str(Path(path))

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    except Exception:
        return os.path.join(os.path.abspath("."), relative_path)

def run_system_command(command, timeout=5, retry=False, delay=5):
    """Run a system command with timeout and retry capability."""
    def target():
        try:
            subprocess.run(command, shell=True, check=True)
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
            run_system_command(command, timeout)

def play_sound(sound_path):
    """Play a sound file in a cross-platform way."""
    try:
        sound_path = normalize_path(sound_path)
        
        if IS_TERMUX:
            run_system_command(f"termux-media-player play {sound_path}", timeout=5, retry=True)
        else:
            try:
                from playsound3 import playsound
                playsound(sound_path, block=False)
            except ImportError:
                print("Error: playsound3 module not found. Please install it using 'pip install playsound3'")
    except Exception as e:
        print(f"Error playing sound: {e}")

def show_notification(title, message, timeout=15):
    """Show a system notification in a cross-platform way."""
    try:
        if IS_TERMUX:
            run_system_command(
                f"termux-notification -t '{title}' -c '{message}' --led-color '#a575ff' --priority 'high'",
                timeout=5, 
                retry=True
            )
        else:
            try:
                from plyer import notification
                notification.notify(
                    title=title,
                    message=message,
                    app_icon=None,
                    timeout=timeout
                )
            except ImportError:
                print("Error: plyer module not found. Please install it using 'pip install plyer'")
    except Exception as e:
        print(f"Error showing notification: {e}")

def check_battery():
    """Check battery level in a cross-platform way."""
    try:
        if IS_TERMUX:
            try:
                import json
                battery_status = os.popen("termux-battery-status").read()
                battery_data = json.loads(battery_status)
                return battery_data["percentage"]
            except Exception as e:
                print(f"Battery check failed: {e}")
                return None
        else:
            try:
                import psutil
                battery = psutil.sensors_battery()
                if battery:
                    return battery.percent
                return None
            except Exception as e:
                print(f"Battery check failed: {e}")
                return None
    except Exception as e:
        print(f"General battery check error: {e}")
        return None

def install_package(package_name):
    """Install a Python package in a cross-platform way."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}")
        return False

def load_env_variables():
    """Load environment variables from .env file if present."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("dotenv module not found. Skipping .env loading.") 