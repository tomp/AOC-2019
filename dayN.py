#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day N
#
from typing import Sequence, Any
from collections import defaultdict
from dataclasses import dataclass
import math
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        """,
        expected1
    ),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text()]

def sample_case(idx: int = 0) -> tuple[Lines, int]:
    text, expected = SAMPLE_CASES[idx]
    lines = load_text(text)
    return lines, expected

## Use these if blank lines should be discarded.

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

## Use these if blank lines in input are meaningful.

def load_text(text: str) -> Lines:
    return [line.strip() for line in text.strip("\n").split("\n")]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        line = line.strip()
        if not line:
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution

def solve(lines: Lines) -> int:
    """Solve the problem."""
    return 0


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    # example2()
    # part2(input_lines)
