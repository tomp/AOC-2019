#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 16
#
from typing import Sequence, Any
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from functools import cache
from math import ceil
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    ("80871224585914546619083218645595", "24176176"),
    ("19617804207202209144916044189917", "73745418"),
    ("69317163492948606335995924319873", "52432133"),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def sample_case(idx: int = 0) -> tuple[Lines, int]:
    text, expected = SAMPLE_CASES[idx]
    lines = load_text(text)
    return lines, expected

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

BASE_PATTERN = [0, 1, 0, -1]
BASE_SIZE = len(BASE_PATTERN)

@cache
def pattern(size: int, idx: int = 0) -> list[int]:
    pattern_size = BASE_SIZE * (idx + 1)
    repeat = ceil(size / pattern_size)
    values = repeat * list(chain(
        *[[BASE_PATTERN[i]] * (idx + 1) for i in (0, 1, 2, 3)]
    ))
    return values[:size]

def phase(inarray: list[int]) -> list[int]:
    result = []
    size = len(inarray)
    for i in range(size):
        patt = pattern(size+1, i)[1:]
        element = sum([v * c for v, c in zip(inarray, patt)])
        result.append(abs(element) % 10)
    return result

def solve(text: str) -> int:
    """Solve the problem."""
    arr = list(map(int, text))
    for _ in range(100):
        arr = phase(arr)
    return "".join(map(str, arr[:8]))


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines[0])
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines[0])
    print(f"result is {result}")
    assert result == "19239468"
    print("= " * 32)


# PART 2

if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    # example2()
    # part2(input_lines)
