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

CONFIG_FILES = [
    "configs/settings.json",
    "configs/global_settings.json",
    "configs/misc.json"
]

prev_configs = {}
for path in CONFIG_FILES:
    try:
        with open(path, "r") as f:
            prev_configs[path] = json.load(f)
    except FileNotFoundError:
        prev_configs[path] = {}

def read_tokens_file():
    try:
        with open("tokens.txt", "r") as tokens_file:
            return tokens_file.read()
    except FileNotFoundError:
        return ""

def write_tokens_file(content):
    with open("tokens.txt", "w") as tokens_file:
        tokens_file.write(content)

def deep_merge(old, new):
    """
    This one merges based on on type of each items, unlike default merge this is much safer.
    """
    result = {}
    for key, new_value in new.items():
        if key in old:
            old_value = old[key]
            if isinstance(old_value, dict) and isinstance(new_value, dict):
                # Recursive
                result[key] = deep_merge(old_value, new_value)
            elif type(old_value) == type(new_value):
                result[key] = old_value
            else:
                result[key] = new_value
        else:
            result[key] = new_value
    return result

def merge_json_carry_over(path, prev_dict):
    with open(path, 'r') as f:
        main_data = json.load(f)

    updated_data = deep_merge(prev_dict, main_data)

    with open(path, 'w') as f:
        json.dump(updated_data, f, indent=4)

def merge_custom_user_settings():
    """
    Merge each <user_id>.settings.json with the new base settings.json.
    Keeps user overrides, adopts new defaults.
    """
    base_path = "configs/settings.json"
    try:
        with open(base_path, "r") as f:
            base_settings = json.load(f)
    except FileNotFoundError:
        # This shouldn't happen since settings.json should always be there in configs folder
        console.log("[red]Base settings.json not found, skipping user settings merge.")
        return

    for filename in os.listdir("configs"):
        if filename.endswith(".settings.json") and filename != "settings.json":
            user_path = os.path.join("configs", filename)
            try:
                with open(user_path, "r") as uf:
                    user_data = json.load(uf)
                console.log(f"[cyan]Merging custom config {filename} with new settings.json...")
                merged_data = deep_merge(user_data, base_settings)
                with open(user_path, "w") as out:
                    json.dump(merged_data, out, indent=4)
            except Exception as e:
                console.log(f"[red]Failed to merge {filename}: {e}")

def pull_latest_changes_git():
    previous_tokens = read_tokens_file()
    repo_dir = "."
    os.chdir(repo_dir)

    # Check for uncommitted changes
    with console.status("[bold green]Checking for uncommitted changes..."):
        status_result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

    if status_result.stdout:
        console.log("[yellow]Uncommitted changes detected. Stashing changes...")
        with console.status("[bold yellow]Stashing changes..."):
            subprocess.run(['git', 'stash'])
            sleep(1)

    # Check for untracked files
    with console.status("[bold cyan]Checking for untracked files..."):
        untracked_files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True)

    if untracked_files.stdout:
        console.log("[yellow]Untracked files detected. Cleaning up untracked files...")
        with console.status("[bold red]Cleaning untracked files..."):
            subprocess.run(['git', 'clean', '-f', "-d"])
            sleep(1)

    with console.status("[bold green]Pulling the latest changes from main branch..."):
        subprocess.run(['git', 'checkout', 'main'])
        subprocess.run(['git', 'pull', 'origin', 'main'])
        sleep(1)

    console.log("[bold green]Update complete!")
    for path in CONFIG_FILES:
        console.log(f"[bold green]Merging previous config into {path}...")
        merge_json_carry_over(path, prev_configs.get(path, {}))

    merge_custom_user_settings()

    write_tokens_file(previous_tokens)
    console.log("[bold green]Previous tokens content restored to tokens.txt!")

# Start
pull_latest_changes_git()
