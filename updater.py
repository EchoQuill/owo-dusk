import os
import json
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.spinner import Spinner
from time import sleep

# Initialize rich console
console = Console()

# Load the previous config JSON
with open("config.json", "r") as config_file:
    prev_config_dict = json.load(config_file)

# Read tokens.txt content before update
def read_tokens_file():
    try:
        with open("tokens.txt", "r") as tokens_file:
            return tokens_file.read()
    except FileNotFoundError:
        return ""

# Write content to tokens.txt after the update
def write_tokens_file(content):
    with open("tokens.txt", "w") as tokens_file:
        tokens_file.write(content)

def merge_json(sub_file=prev_config_dict):
    # Load the main and sub JSON files
    with open("config.json", 'r') as main:
        main_data = json.load(main)
    
    # Merge the JSON files
    for key in main_data:
        if key in prev_config_dict:
            main_data[key] = prev_config_dict[key]
    
    # Save the merged JSON to the output file
    with open("config.json", 'w') as output:
        json.dump(main_data, output, indent=4)

def pull_latest_changes_git():
    previous_tokens = read_tokens_file()
    repo_dir = "."  # Update with your repository directory if needed

    # Change to the repository directory
    os.chdir(repo_dir)

    # Spinner for checking uncommitted changes
    with console.status("[bold green]Checking for uncommitted changes...") as status:
        status_result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    
    if status_result.stdout:
        console.log("[yellow]Uncommitted changes detected. Stashing changes...")

        # Spinner for stashing changes
        with console.status("[bold yellow]Stashing changes...") as status:
            subprocess.run(['git', 'stash'])
            sleep(1)  # Simulate some delay

    # Spinner for checking untracked files
    with console.status("[bold cyan]Checking for untracked files...") as status:
        untracked_files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True)

    if untracked_files.stdout:
        console.log("[yellow]Untracked files detected. Cleaning up untracked files...")

        # Spinner for cleaning untracked files
        with console.status("[bold red]Cleaning untracked files...") as status:
            subprocess.run(['git', 'clean', '-f', "-d"])  # Automatically remove untracked files
            sleep(1)  # Simulate some delay

    # Spinner for pulling latest changes
    with console.status("[bold green]Pulling the latest changes from origin/main...") as status:
        subprocess.run(['git', 'checkout', 'main'])  # Make sure we're on the correct branch
        subprocess.run(['git', 'pull', 'origin', 'main'])  # Pull the latest changes
        sleep(1)  # Simulate some delay

    console.log("[bold green]Update complete!")

    console.log("[bold green]Attempting to merge previous config with the updated config...")
    merge_json()

    # After update, restore tokens.txt content
    write_tokens_file(previous_tokens)    # Replace with previous content

    console.log("[bold green]Previous tokens content restored to tokens.txt!")

# Call the function to pull the latest changes and merge JSON
pull_latest_changes_git()
