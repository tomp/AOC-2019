#!/usr/bin/env python3
"""
Download some day's input from the AOC site.
This requires a session key for a particular user's account.
"""
from pathlib import Path
import argparse

import requests

SESSION_KEY = "session_key.txt"
SITE = "https://adventofcode.com/2019"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, help="Day number (eg '3')")
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_args()
    url = f"{SITE}/day/{opt.day}/input"
    # print(f"URL: {url}")

    session_key = Path(SESSION_KEY).read_text().strip()

    s = requests.Session()

    resp = s.get(url, cookies={'session': session_key})
    # print(f"OK: {resp.ok}")

    print(resp.content.decode())


if __name__ == '__main__':
    main()

