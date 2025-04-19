# OwO Dusk

![Version](https://img.shields.io/badge/version-2.0.2-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-green)

A cross-platform Discord bot for OwO grinding that works on Windows, macOS, and Linux.

## Cross-Platform Support

OwO Dusk now supports multiple operating systems:

- Windows
- macOS
- Linux (Ubuntu, Fedora, Arch, etc.)
- Android (via Termux)

## Requirements

- Python 3.8 or higher
- Internet connection
- Discord account with token

## Installation

### Windows

1. Make sure you have Python 3.8+ installed
2. Clone or download this repository
3. Run `python setup.py` in your terminal/command prompt

### macOS

1. Make sure you have Python 3.8+ installed
   ```
   brew install python
   ```
2. Clone or download this repository
3. Run `python3 setup.py` in your terminal

### Linux

1. Make sure you have Python 3.8+ installed
   ```
   # Debian/Ubuntu
   sudo apt update
   sudo apt install python3 python3-pip

   # Fedora
   sudo dnf install python3 python3-pip

   # Arch
   sudo pacman -S python python-pip
   ```
2. Clone or download this repository
3. Run `python3 setup.py` in your terminal

### Android (Termux)

1. Install Termux from F-Droid (not Play Store)
2. Install required packages:
   ```
   pkg update
   pkg install python git
   ```
3. Clone this repository:
   ```
   git clone https://github.com/EchoQuill/owo-dusk
   ```
4. Enter the directory and run setup:
   ```
   cd owo-dusk
   python setup.py
   ```

## Usage

After installation:

1. Edit your tokens in `tokens.txt`
2. Configure settings in `config.json`
3. Run the bot using the appropriate script:
   - **Windows**: Double-click on `run.bat` or run `python uwu.py` in command prompt
   - **macOS/Linux**: Run `./run.sh` or `python3 uwu.py` in terminal
   - **Termux**: Run `./run.sh` or `python uwu.py` in Termux

Alternatively, you can run directly with Python:
```
# Windows
python uwu.py

# macOS/Linux/Termux
python3 uwu.py
```

## Features

- Auto hunt, battle and owo
- Auto pray/curse
- Auto lootbox and crate opening
- Captcha detection with notifications
- Web dashboard for stats and configuration
- Cross-platform support
- And much more!

## Troubleshooting

### Linux Audio Issues

If you encounter issues with audio notifications on Linux:

1. Make sure you have the required system libraries:
   ```
   # Debian/Ubuntu
   sudo apt install libasound2-dev libportaudio2

   # Fedora
   sudo dnf install alsa-lib-devel portaudio-devel

   # Arch
   sudo pacman -S alsa-lib portaudio
   ```

2. Check your sound system configuration:
   ```
   # For PulseAudio
   pulseaudio --check

   # For PipeWire
   systemctl --user status pipewire
   ```

### macOS Notification Issues

If notifications aren't working on macOS:

1. Make sure Python has permission to send notifications in System Preferences > Notifications
2. Install additional dependencies if needed:
   ```
   pip3 install pyobjc-framework-Cocoa
   ```

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

<div align="center">
  <center><img src="static/imgs/logo.png" width="150"></center>
  <br>
  <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Pacifico&size=40&pause=1000&color=802DF7&center=true&vCenter=true&random=false&width=425&lines=Owo+Dusk" alt="Typing SVG" />
  <br/>
  <a href="https://discord.gg/hDDrKhWPqr"><img src="https://invidget.switchblade.xyz/hDDrKhWPqr" alt="Discord Invite"/> </a>
  <br/>
  <p>join our discord! (Join with an **CLEAN** alt please , one that hasn't and won't use owobot!)</p>
  <p>Alternatively, send a friend request to `@echoquill` on discord for help!</p>
</div>


---

Supports BOTH MOBILE AND DESKTOP with captcha Notifiers for both. And we also support reaction bot, and have a custom dashboard for solving captchas (image ones) through your browser!

> [!IMPORTANT]
> ⚠️🚨 WE ARE NOT responsible if you get banned using our selfbots. Selfbots are agains discord tos and also breaks owo bots rules. If you do plan on using it still then atleast take some steps to ensure that you won't be getting banned like no more than one/two account grinding in one servers, Only grinding in pricate servers, And not openly sharing the fact that you use selfbot to grind owo.


---
# Basic installation
---
* Computer
  ```
  git clone https://github.com/echoquill/owo-dusk.git && cd owo-dusk && python setup.py
  ```
  > make sure git and python is installed and that terminal is open in `Desktop` for easier access
* Termux
  ```
  pkg update && pkg upgrade -y && termux-setup-storage && pkg install python -y && pkg install git -y && pkg install termux-api -y && cd storage/downloads && git clone https://github.com/echoquill/owo-dusk.git && cd owo-dusk && python setup.py
  ```
  > Make sure to install termux and termux:api app from fdroid or github.
  
  after the above is done, do the steps setup.py asks you to.

> [!TIP]
> For help with setup, please join our discord server(or send `echoquill` a friend request) and I'll help you set it up on both termux(android) and desktop/laptop devices. Ill make tutoriales for it laters!


---
# Screenshots 📸 
---

<div align="center">
  <center><img src="static/imgs/desktop_cli.png" width="800" height="500"></center>
  <br>
  <p>Desktop CLI screenshot</p>
  <br>
  <center><img src="static/imgs/website.png" width="1200" height=600"></center>
  <br>
  <p>Website for captcha logger.</p>
</div>

---
# development 🖥️
---

<div>
    <center><img src="https://repobeats.axiom.co/api/embed/0a1054d566f34198e5adb680c8c95884f514b0bc.svg" alt="Alt" title="Repobeats analytics image"></div></center>
</div>

---

thanks for reading :>, I hope this tool could help you even if a little ❤ .
