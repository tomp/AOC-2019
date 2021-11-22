#!/usr/bin/env python3
#
#  Advent of Code 2019 - day 5
#
from pathlib import Path
from intcode import init_mem, run_intcode

INPUTFILE = "input.txt"

# Utility functions

## Use these if blank lines should be discarded.
def sample_input() -> list[str]:
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))


def load_input(infile) -> list[str]:
    return filter_blank_lines(Path(infile).open())


def filter_blank_lines(lines) -> list[str]:
    return [line.strip() for line in lines if line.strip()]


# Solution

def solve(lines):
    """Solve the problem."""
    mem = init_mem(lines[0].strip())
    inp = [1]
    out = []
    final = run_intcode(mem, inp, out)
    print(f"output: {', '.join([str(v) for v in out])}")
    return out[-1]


def solve2(lines):
    """Solve the problem."""
    mem = init_mem(lines[0].strip())
    inp = [5]
    out = []
    final = run_intcode(mem, inp, out)
    print(f"output: {', '.join([str(v) for v in out])}")
    return out[-1]


# PART 1

def part1(lines):
    print("PART 1:")
    result = solve(lines)
    assert result == 14155342
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def part2(lines):
    print("PART 1:")
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    lines = load_input(INPUTFILE)
    part1(lines)
    part2(lines)
