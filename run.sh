#!/bin/bash

# OwO-dusk runner script for Linux/Mac
# This script helps run owo-dusk on Unix-based systems

# Functions
check_dependencies() {
  echo "Checking dependencies..."
  
  # Check Python
  if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
  fi
  
  # Check pip
  if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3."
    exit 1
  fi
  
  # Check git
  if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install Git to enable updates."
  fi
  
  echo "All core dependencies are available."
}

setup_environment() {
  echo "Setting up environment..."
  
  # Create virtual environment if it doesn't exist
  if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
  fi
  
  # Activate virtual environment
  if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
  else
    echo "Virtual environment not found. Running without it."
  fi
  
  # Install requirements
  echo "Installing/updating requirements..."
  pip3 install -r requirements.txt
}

run_application() {
  echo "Starting OwO-dusk..."
  python3 uwu.py
}

# Main execution
check_dependencies
setup_environment
run_application 