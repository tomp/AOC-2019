#!/usr/bin/env python3
#
#  Advent of Code 2019 - day 1
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
1969
100756
"""

# Utility functions

## Use these if blank lines should be discarded.
def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))

def load_input(infile):
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

def fuel_required(mass):
    return max((int(mass) // 3) - 2, 0)

def fuel_required2(mass):
    result = 0
    fuel = max((int(mass) // 3) - 2, 0)
    while fuel:
        result += fuel
        fuel = max((fuel // 3) - 2, 0)
    return result

def solve(lines):
    """Solve the problem."""
    total_fuel = 0
    for line in lines:
        total_fuel += fuel_required(int(line))
    return total_fuel

def solve2(lines):
    """Solve the problem."""
    total_fuel = 0
    for line in lines:
        total_fuel += fuel_required2(int(line))
    return total_fuel


# PART 1

def example1():
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve(lines)
    expected = 34237
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 3324332
    print("= " * 32)


# PART 2

SAMPLE_CASES2 = [
    (14, 2),
    (1969, 966),
    (100756, 50346),
]

def example2():
    """Run example for problem with input lines."""
    print("EXAMPLE 2:")
    for arg, expected in SAMPLE_CASES2:
        result = fuel_required2(arg)
        print(f"'sample-input' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)


def part2(lines):
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
