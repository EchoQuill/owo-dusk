@echo off
REM Run script for OwO Dusk on Windows

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2 delims=." %%a in ('python -c "import sys; print(sys.version.split()[0])"') do (
    set PYTHON_VERSION=%%a
)

REM Run setup if needed
if not exist config.json (
    echo It looks like this is your first time running OwO Dusk
    echo Running setup...
    python setup.py
)

REM Run the main script
echo Starting OwO Dusk...
python uwu.py

pause 