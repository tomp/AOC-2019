#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 9
#
from pathlib import Path
from intcode import IntCode

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99",
        "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    ),
    (
        "1102,34915192,34915192,7,4,7,99,0",
        "1219070632396864"
    ),
    (
        "104,1125899906842624,99",
        "1125899906842624"
    ),
]


# Utility functions

## Use these if blank lines should be discarded.
def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))

def load_input(infile):
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


## Use these if blank lines in input are meaningful.
def sample_input():
    return SAMPLE_INPUT.strip("\n").split("\n")

def load_input(infile):
    return [line.strip() for line in Path(infile).open()]

def parse_sections(lines):
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

def solve2(line):
    """Solve the problem."""
    proc = IntCode(line)
    proc.input(2)
    proc.run()
    output = []
    out = proc.output()
    while out is not None:
        output.append(str(out))
        out = proc.output()
    return ",".join(output)

def solve(line):
    """Solve the problem."""
    proc = IntCode(line)
    proc.input(1)
    proc.run()
    output = []
    out = proc.output()
    while out is not None:
        output.append(str(out))
        out = proc.output()
    return ",".join(output)


# PART 1

def example1():
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for arg, expected in SAMPLE_CASES:
        result = solve(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines):
    print("PART 1:")
    result = solve(lines[0])
    print(f"result is {result}")
    assert result == "2752191671"
    print("= " * 32)


# PART 2

def part2(lines):
    print("PART 2:")
    result = solve2(lines[0])
    print(f"result is {result}")
    assert result == "87571"
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    part2(lines)
