#!/usr/bin/env python3
#
#  Advent of Code 2019 - day 4
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
"""

SAMPLE_CASES = [
    ("111111", True),
    ("223450", False),
    ("123789", False),
]

SAMPLE_CASES2 = [
    ("112233", True),
    ("123444", False),
    ("111122", True),
]

INPUT = "158126-624574"


# Solution

def is_valid2(password: int) -> bool:
    digits = str(password)
    assert len(digits) == 6
    last = digits[0]
    double = False
    repeat = 0
    for digit in digits[1:]:
        if digit == last:
            repeat += 1
        else:
            double |= repeat == 1
            repeat = 0
        if int(digit) < int(last):
            return False
        last = digit
    double |= repeat == 1
    return double


def is_valid(password: int) -> bool:
    digits = str(password)
    assert len(digits) == 6
    last = digits[0]
    double = False
    for digit in digits[1:]:
        if digit == last:
            double = True
        if int(digit) < int(last):
            return False
        last = digit
    return double


def solve2(text):
    """Solve the problem."""
    low, high = [int(v) for v in text.split("-")]
    print(f"range: {low} - {high}")
    count = 0
    for password in range(low, high+1):
        if is_valid2(password):
            count += 1
    return count


def solve(text):
    """Solve the problem."""
    low, high = [int(v) for v in text.split("-")]
    print(f"range: {low} - {high}")
    count = 0
    for password in range(low, high+1):
        if is_valid(password):
            count += 1
    return count


# PART 1

def example1():
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for arg, expected in SAMPLE_CASES:
        result = is_valid(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)


def part1(line):
    print("PART 1:")
    result = solve(line)
    assert result == 1665
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for arg, expected in SAMPLE_CASES2:
        result = is_valid2(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)


def part2(line):
    print("PART 2:")
    result = solve2(line)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    part1(INPUT)
    example2()
    part2(INPUT)
