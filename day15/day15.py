#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 15
#
from typing import Sequence, Any
from collections import defaultdict
from dataclasses import dataclass
import math
from pathlib import Path

from intcode import IntCode, MockIntCode
from droid import Droid

INPUTFILE = "input.txt"

Lines = Sequence[str]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    proc = IntCode(lines[0])
    droid = Droid(proc)
    done = droid.run(complete_map=True)
    return droid.oxygen_fill_time()

def solve(lines: Lines) -> int:
    """Solve the problem."""
    proc = IntCode(lines[0])
    droid = Droid(proc)
    done = droid.run()
    return droid.shortest_path()


# PART 1

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 230
    print("= " * 32)

# PART 2

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 288
    print("= " * 32)


if __name__ == "__main__":
    # example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    part2(input_lines)
