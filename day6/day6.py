#!/usr/bin/env python3
#
#  Advent of Code 2019 - day 6
#
from pathlib import Path
from collections import defaultdict

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

SAMPLE_INPUT2 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
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

def parse_input(lines: list[str]) -> dict[str, list[str]]:
    """Parse the input and return a dict mapping each object to
    a list of the objects that are directly in its orbit.
    """
    satellites = defaultdict(list)
    for line in lines:
        if not line.strip():
            continue
        center, satellite = [v.strip() for v in line.strip().split(")")]
        satellites[center].append(satellite)
    return satellites

def build_graph(satellites):
    neighbors = defaultdict(list)
    neighbors["COM"] = satellites["COM"]
    bodies = [(satellite, "COM") for satellite in satellites["COM"]]
    while bodies:
        body, center = bodies.pop(0)
        neighbors[body] = satellites[body] + [center]
        for satellite in satellites[body]:
            bodies.append((satellite, body))
    return neighbors


def solve2(lines):
    """Solve the problem."""
    satellites = parse_input(lines)
    neighbors = build_graph(satellites)

    # Breadth-first search for shortest path between YOU and SAN
    bodies = [(nayb, 1) for nayb in neighbors["YOU"]]
    visited = set(["YOU"])
    while bodies:
        body, dist = bodies.pop(0)
        visited.add(body)
        if body == "SAN":
            return dist - 2
        for nayb in neighbors[body]:
            if nayb not in visited:
                bodies.append((nayb, dist + 1))
    # we should never exit the search without finding SAN
    return None


def solve(lines):
    """Solve the problem."""
    satellites = parse_input(lines)
    count = 0
    bodies = [("COM", 0)]
    while bodies:
        body, orbits = bodies.pop(0)
        count += orbits
        for satellite in satellites[body]:
            bodies.append((satellite, orbits + 1))
    return count

# PART 1

def example1():
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve(lines)
    expected = 42
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 268504
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input lines."""
    print("EXAMPLE 2:")
    lines = filter_blank_lines(SAMPLE_INPUT2.split("\n"))
    result = solve2(lines)
    expected = 4
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part2(lines):
    print("PART 2:")
    result = solve2(lines)
    assert result == 409
    print(f"result is {result}")
    print("= " * 32)



if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
