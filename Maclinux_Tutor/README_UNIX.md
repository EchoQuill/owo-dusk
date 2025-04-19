# OwO-Dusk for Linux and macOS

This guide will help you set up and run OwO-Dusk on Unix-based systems (Linux and macOS).

## Prerequisites

- Python 3.8 or higher
- pip3
- Git (for updates)
- For notifications on Linux: `notify-send` (part of `libnotify-bin` package)
- For battery monitoring on Linux: `psutil` or `/sys/class/power_supply/BAT0/capacity` access

## Installation

1. Clone the repository (if you haven't already):
   ```bash
   git clone https://github.com/EchoQuill/owo-dusk.git
   cd owo-dusk
   ```

2. Run the setup script:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   This script will:
   - Check for required dependencies
   - Set up a Python virtual environment (recommended)
   - Install all necessary packages
   - Start the application

## Manual Setup (Alternative)

If you prefer to set up manually:

1. Install requirements:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Configure your tokens:
   - Edit the `tokens.txt` file with your Discord token and channel ID

3. Run the application:
   ```bash
   python3 uwu.py
   ```

## Platform-Specific Features

### Notifications
- **macOS**: Uses `osascript` for native notifications (falls back to tkinter)
- **Linux**: Uses `notify-send` for desktop notifications (falls back to tkinter)

### Battery Monitoring
- **macOS**: Uses `psutil` or `system_profiler` for battery information
- **Linux**: Uses `psutil` or reads from `/sys/class/power_supply/BAT0/capacity`

## Troubleshooting

### Common Issues

1. **ImportError for tkinter**:
   ```bash
   # On Debian/Ubuntu
   sudo apt-get install python3-tk
   
   # On Fedora
   sudo dnf install python3-tkinter
   
   # On macOS with Homebrew
   brew install python-tk
   ```

2. **Notification issues on Linux**:
   ```bash
   sudo apt-get install libnotify-bin   # Debian/Ubuntu
   sudo dnf install libnotify           # Fedora
   ```

3. **Battery monitoring issues**:
   ```bash
   pip3 install psutil
   ```

### Running on Headless Servers

If you're running on a server without a GUI, you can disable the popup/notification features in the config.json file:

```json
"captcha": {
  "toastOrPopup": false
}
```

## Updates

To update the application, you can either:

1. Use the built-in updater:
   ```bash
   python3 updater.py
   ```

2. Or pull the latest changes manually:
   ```bash
   git pull
   pip3 install -r requirements.txt
   ```

## Support

If you encounter any issues specific to Unix-based systems, please report them in the GitHub repository. 