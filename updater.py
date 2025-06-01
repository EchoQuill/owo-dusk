# This file is part of owo-dusk.
#
# Copyright (c) 2024-present EchoQuill
#
# Portions of this file are based on code by EchoQuill, licensed under the
# GNU General Public License v3.0 (GPL-3.0).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import os
import json
import subprocess
from rich.console import Console
from time import sleep

console = Console()

# Load the previous config
with open("config.json", "r") as config_file:
    prev_config_dict = json.load(config_file)

def read_tokens_file():
    try:
        with open("tokens.txt", "r") as tokens_file:
            return tokens_file.read()
    except FileNotFoundError:
        return ""

def write_tokens_file(content):
    with open("tokens.txt", "w") as tokens_file:
        tokens_file.write(content)

def deep_merge_carry_over(base, new):
    result = {}

    for key, value in new.items():
        if key in base:
            if isinstance(value, dict) and isinstance(base[key], dict):
                result[key] = deep_merge_carry_over(base[key], value)
            else:
                # Use the existing value from base
                result[key] = base[key]
        else:
            # Use the default value from new
            result[key] = value

    return result

def merge_json_carry_over():
    with open("config.json", 'r') as main_file:
        main_data = json.load(main_file)

    updated_data = deep_merge_carry_over(prev_config_dict, main_data)

    with open("config.json", 'w') as output_file:
        json.dump(updated_data, output_file, indent=4)

def pull_latest_changes_git():
    previous_tokens = read_tokens_file()
    repo_dir = "."
    os.chdir(repo_dir)

    # Check for uncommitted changes
    with console.status("[bold green]Checking for uncommitted changes...") as status:
        status_result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

    if status_result.stdout:
        console.log("[yellow]Uncommitted changes detected. Stashing changes...")
        with console.status("[bold yellow]Stashing changes...") as status:
            subprocess.run(['git', 'stash'])
            sleep(1)

    # Check for untracked files
    with console.status("[bold cyan]Checking for untracked files...") as status:
        untracked_files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True)

    if untracked_files.stdout:
        console.log("[yellow]Untracked files detected. Cleaning up untracked files...")
        with console.status("[bold red]Cleaning untracked files...") as status:
            subprocess.run(['git', 'clean', '-f', "-d"])
            sleep(1)

    # Pull the latest changes
    with console.status("[bold green]Pulling the latest changes from origin/main...") as status:
        subprocess.run(['git', 'checkout', 'main'])
        subprocess.run(['git', 'pull', 'origin', 'main'])
        sleep(1)

    # Merge configuration and restore tokens
    console.log("[bold green]Update complete!")
    console.log("[bold green]Attempting to merge previous config with the updated config...")
    merge_json_carry_over()
    write_tokens_file(previous_tokens)
    console.log("[bold green]Previous tokens content restored to tokens.txt!")



# Run the update process
#pull_latest_changes_git()

print("HiHi, updater broken. For steps to update, check github! Sorry, was busy so couldn't finish a fix for updater")