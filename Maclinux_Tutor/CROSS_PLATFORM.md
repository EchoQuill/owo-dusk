# Cross-Platform Compatibility Changes

This document summarizes the changes made to make OwO-Dusk compatible with Linux and macOS operating systems.

## Files Modified

1. **uwu.py**:
   - Enhanced `resource_path()` function to handle paths correctly on all platforms
   - Improved battery monitoring for Linux and macOS systems
   - Added additional signal handlers for Unix-like systems
   - Updated the popup notification system with platform-specific implementations
     - macOS: Uses `osascript` for native notifications
     - Linux: Uses `notify-send` for desktop notifications
     - Fallback to tkinter for all platforms

2. **updater.py**:
   - Added checks for Git installation with platform-specific installation instructions
   - Improved error handling for cross-platform compatibility

3. **setup.py**:
   - Added platform detection functions: `is_macos()` and `is_linux()`
   - Added platform-specific package installation:
     - For Linux (Debian/Ubuntu): `apt-get` to install required packages
     - For Linux (Fedora/RHEL): `dnf` to install required packages
     - For macOS: Homebrew to install required packages

## New Files Added

1. **run.sh**:
   - Bash script for Unix-based systems (Linux and macOS)
   - Checks for required dependencies
   - Sets up Python virtual environment
   - Installs necessary packages
   - Launches the application

2. **README_UNIX.md**:
   - Comprehensive guide for Linux and macOS users
   - Installation instructions
   - Platform-specific features explained
   - Troubleshooting common issues
   - Instructions for headless servers

## Platform-Specific Features

### Notifications
- **Windows**: Uses tkinter popups
- **macOS**: Uses `osascript` for native notifications (falls back to tkinter)
- **Linux**: Uses `notify-send` for desktop notifications (falls back to tkinter)

### Battery Monitoring
- **Windows**: Uses `psutil`
- **macOS**: Uses `psutil` or `system_profiler`
- **Linux**: Uses `psutil` or reads from `/sys/class/power_supply/BAT0/capacity`
- **Termux**: Uses `termux-battery-status`

### Signal Handling
- Added platform-specific signal handlers for graceful termination
- Windows: SIGINT
- Unix-like systems: SIGINT, SIGTERM, SIGHUP

## How to Use

1. **On Windows**:
   - No changes to the original procedure
   
2. **On Linux/macOS**:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

## Testing

The changes have been designed to be backward compatible, maintaining the original functionality on Windows while adding support for Linux and macOS. The code has been structured to gracefully fallback to alternative methods when platform-specific features are not available. 