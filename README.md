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
