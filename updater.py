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

def merge_json(sub_file=prev_config_dict):
    with open("config.json", 'r') as main:
        main_data = json.load(main)
    
    for key in main_data:
        if key in prev_config_dict:
            main_data[key] = prev_config_dict[key]
    
    with open("config.json", 'w') as output:
        json.dump(main_data, output, indent=4)

def pull_latest_changes_git():
    previous_tokens = read_tokens_file()
    repo_dir = "."
    os.chdir(repo_dir)

    with console.status("[bold green]Checking for uncommitted changes...") as status:
        status_result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    
    if status_result.stdout:
        console.log("[yellow]Uncommitted changes detected. Stashing changes...")
        with console.status("[bold yellow]Stashing changes...") as status:
            subprocess.run(['git', 'stash'])
            sleep(1)

    with console.status("[bold cyan]Checking for untracked files...") as status:
        untracked_files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True)

    if untracked_files.stdout:
        console.log("[yellow]Untracked files detected. Cleaning up untracked files...")
        with console.status("[bold red]Cleaning untracked files...") as status:
            subprocess.run(['git', 'clean', '-f', "-d"])
            sleep(1)

    with console.status("[bold green]Pulling the latest changes from origin/main...") as status:
        subprocess.run(['git', 'checkout', 'main'])
        subprocess.run(['git', 'pull', 'origin', 'main'])
        sleep(1)

    console.log("[bold green]Update complete!")
    console.log("[bold green]Attempting to merge previous config with the updated config...")
    merge_json()
    write_tokens_file(previous_tokens)
    console.log("[bold green]Previous tokens content restored to tokens.txt!")

pull_latest_changes_git()
