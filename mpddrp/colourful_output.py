#!/usr/bin/env python3
"""provides functions for colourful terminal output"""

import colorama

def success(message):
    """prints out the provided message in green"""

    print(f"{colorama.Fore.GREEN}{message}{colorama.Style.RESET_ALL}")
def error(message):
    """prints out the provided message in red"""

    print(f"{colorama.Fore.RED}{message}{colorama.Style.RESET_ALL}")
def info(message):
    """prints out the provided message in magenta"""

    print(f"{colorama.Fore.MAGENTA}{message}{colorama.Style.RESET_ALL}")
