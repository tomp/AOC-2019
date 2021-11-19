#!/usr/bin/env python3
#
#  Advent of Code 2019 - day 3
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
"""

SAMPLE_CASES = [
    (("R8,U5,L5,D3",
      "U7,R6,D4,L4"),
      6
    ),
    (("R75,D30,R83,U83,L12,D49,R71,U7,L72",
      "U62,R66,U55,R34,D71,R55,D58,R83"),
      159
    ),
    (("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
      "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"),
      135
    ),
]

SAMPLE_CASES2 = [
    (("R8,U5,L5,D3",
      "U7,R6,D4,L4"),
      30
    ),
    (("R75,D30,R83,U83,L12,D49,R71,U7,L72",
      "U62,R66,U55,R34,D71,R55,D58,R83"),
      610
    ),
    (("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
      "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"),
      410
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


# Solution

Directions = list[tuple[str, int]]
Coords = tuple[int, int]

def parse_path(line: str) -> Directions:
    return [(item[0], int(item[1:])) for item in line.split(",")]

def trace_path(path: Directions) -> set[Coords]:
    x, y = 0, 0
    loc = dict()
    steps = 0
    for direction, dist in path:
        if direction == "U":
            for _ in range(1, dist+1):
                steps += 1
                y += 1
                if (x, y) not in loc:
                    loc[(x, y)] = steps
        elif direction == "D":
            for _ in range(1, dist+1):
                steps += 1
                y -= 1
                if (x, y) not in loc:
                    loc[(x, y)] = steps
        elif direction == "R":
            for _ in range(1, dist+1):
                steps += 1
                x += 1
                if (x, y) not in loc:
                    loc[(x, y)] = steps
        elif direction == "L":
            for _ in range(1, dist+1):
                steps += 1
                x -= 1
                if (x, y) not in loc:
                    loc[(x, y)] = steps
    return loc


def solve2(lines):
    """Solve the problem."""
    path1 = trace_path(parse_path(lines[0]))
    path2 = trace_path(parse_path(lines[1]))
    dist = min([path1[(x, y)] + path2[(x, y)] for x, y in set(path1.keys()) & set(path2.keys())])
    return dist


def solve(lines):
    """Solve the problem."""
    path1 = trace_path(parse_path(lines[0]))
    path2 = trace_path(parse_path(lines[1]))
    dist = min([abs(x) + abs(y) for x, y in set(path1.keys()) & set(path2.keys())])
    return dist


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
    assert len(lines) == 2
    result = solve(lines)
    assert result == 1084
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for arg, expected in SAMPLE_CASES2:
        result = solve2(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)


def part2(lines):
    print("PART 2:")
    assert len(lines) == 2
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
