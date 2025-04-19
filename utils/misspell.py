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

import random
import string

"""
Reference -> https://github.com/GeorgVetterGit/typo_generator/blob/main/TypoCreator.py
"""

keyboard_neighbors = {
    'a': ['q', 'w', 's'], 'b': ['v', 'n'], 'c': ['x', 'v'], 'd': ['s', 'f'],
    'e': ['w', 'r'], 'f': ['d', 'g'], 'g': ['f', 'h'], 'h': ['g', 'j'],
    'i': ['u', 'o'], 'j': ['h', 'k'], 'k': ['j', 'l'], 'l': ['k'],
    'm': ['n'], 'n': ['b', 'm'], 'o': ['i', 'p'], 'p': ['o'],
    'q': ['w', 'a'], 'r': ['e', 't'], 's': ['a', 'd'], 't': ['r', 'y'],
    'u': ['y', 'i'], 'v': ['c', 'b'], 'w': ['q', 'e'], 'x': ['z', 'c'],
    'y': ['t', 'u'], 'z': ['x']
}


def swap_letter(word):
    if len(word) < 2:
        return word
    idx = random.randint(0, len(word) - 2)
    return word[:idx] + word[idx+1] + word[idx] + word[idx+2:]

def replace_with_neighbor(word):
    idx = random.randint(0, len(word) - 1)
    letter = word[idx].lower()
    if letter in keyboard_neighbors:
        new_letter = random.choice(keyboard_neighbors[letter])
        return word[:idx] + new_letter + word[idx+1:]
    return word

def double_letter(word):
    parts = word.split(" ", 1)
    first_word = parts[0]
    idx = random.randint(0, len(first_word) - 1)
    first_word = first_word[:idx] + first_word[idx] + first_word[idx] + first_word[idx+1:]
    return first_word + (" " + parts[1] if len(parts) > 1 else "")

def one_out(word):
    if len(word) < 2:
        return word
    idx = random.randint(0, len(word) - 1)
    return word[:idx] + word[idx+1:]

def add_random_end_noise(word):
    return word + random.choice(string.ascii_letters.lower())

def misspell_word(word):
    typo_functions = {
        40: replace_with_neighbor,
        20: swap_letter,
        25: one_out,
        10: double_letter,
        5: add_random_end_noise
    }

    percentage = random.randint(1,100)

    cumulative = 0
    for probability, function in typo_functions.items():
        cumulative += probability
        if percentage <= cumulative:
            return function(word)
    # Fallback
    return replace_with_neighbor(word)
