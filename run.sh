#!/bin/bash

# Run script for OwO Dusk on Unix-based systems (macOS, Linux, etc.)

# Check if Python 3 is installed
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if Python version is 3.8+
PYTHON_VERSION=$($PYTHON -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "Error: Python version 3.8+ is required, but you have $PYTHON_VERSION"
    echo "Please upgrade your Python installation and try again"
    exit 1
fi

# Check if running on termux
if [ -d "/data/data/com.termux" ] || [[ "$PREFIX" == *"com.termux"* ]]; then
    echo "Detected Termux environment..."
    echo "Checking for termux-specific dependencies..."
    if ! command -v termux-battery-status &>/dev/null; then
        echo "Installing termux-api package..."
        pkg install termux-api -y
    fi
fi

# Check if setup needs to be run
if [ ! -f "config.json" ]; then
    echo "It looks like this is your first time running OwO Dusk"
    echo "Running setup..."
    $PYTHON setup.py
fi

# Run the main script
echo "Starting OwO Dusk..."
$PYTHON uwu.py 