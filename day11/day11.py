#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 11
#
from typing import Sequence, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
from intcode import IntCode

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
"""

# Types

Lines = Sequence[str]
Matrix = Sequence[Sequence[str]]


# Utility functions

def load_input(infile: str) -> Lines:
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


# Solution

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
BLACK, WHITE = 0, 1
COLOR = {BLACK: ".", WHITE: "#"}

@dataclass(frozen=True)
class Location:
    """A Location instance represents a location on a grid.
    Internally, it's reprsented using (row, column) coordinates
    """
    r: int
    c: int

    def move(self, direction: int):
        if direction == UP:
            return Location(self.r - 1, self.c)
        if direction == DOWN:
            return Location(self.r + 1, self.c)
        if direction == RIGHT:
            return Location(self.r, self.c + 1)
        if direction == LEFT:
            return Location(self.r, self.c - 1)
        raise ValueError(f"unsupported direction '{direction}'")


class Hull:
    def __init__(self):
        self.colors = defaultdict(int)
        self.painted = set()

    def color(self, loc: Location, new_color: Optional[int] = None) -> int:
        """Get (or set) the color at the specified location."""
        if new_color is not None:
            self.colors[loc] = new_color
            self.painted.add(loc)
        return self.colors[loc]

    def panels_painted(self) -> int:
        return len(self.painted)

    def bounds(self) -> tuple[int, int, int, int]:
        if not self.colors:
            return 0, 0, 0, 0
        rmin = min([loc.r for loc in self.colors.keys()])
        rmax = max([loc.r for loc in self.colors.keys()])
        cmin = min([loc.c for loc in self.colors.keys()])
        cmax = max([loc.c for loc in self.colors.keys()])
        return rmin, rmax, cmin, cmax

    def dimensions(self) -> tuple[int, int]:
        rmin, rmax, cmin, cmax = self.bounds()
        return rmax - rmin + 1, cmax - cmin + 1

    def print(self):
        rmin, rmax, cmin, cmax = self.bounds()
        for r in range(rmin, rmax+1):
            row = []
            for c in range(cmin, cmax+1):
                row.append(COLOR[self.colors[Location(r, c)]])
            print("".join(row))


class Robot:

    def __init__(self, proc: IntCode):
        self.direction = UP
        self.loc: Location = Location(0, 0)
        self.hull = Hull()
        self.proc = proc

    def run(self) -> None:
        done = False
        while not done:
            done = self.step()

    def step(self) -> bool:
        self.proc.input(self.hull.color(self.loc))
        done = self.proc.run()
        color = self.proc.output()
        if color is not None:
            self.hull.color(self.loc, color)
            turn = self.proc.output()
            self.direction = (self.direction + (2 * turn - 1)) % 4
            self.loc = self.loc.move(self.direction)
        return done

    def panels_painted(self) -> int:
        return self.hull.panels_painted()

class MockIntCode:
    def __init__(self, inp: list[int], out: list[Any]):
        self.inp = inp
        self.out = [[]] + out

    def input(self, value: int) -> None:
        assert value == self.inp[0]
        self.inp.pop(0)

    def run(self) -> bool:
        if self.out:
            self.out = self.out[1:]

    def output(self):
        if self.out[0]:
            return self.out[0].pop(0)
        return None


def test_robot() -> int:
    """Solve the problem."""
    proc = MockIntCode(
        inp=[0, 0, 0, 0, 1, 0, 0], 
        out=[[1, 0], [0, 0], [1, 0], [1, 0], [0, 1], [1, 0], [1, 0]])
    robot = Robot(proc)
    for step in range(7):
        print(f"==== step {step+1}  loc: {robot.loc}  dir: {robot.direction}")
        robot.hull.print()
        robot.step()
    print(f"==== FINAL  loc: {robot.loc}  dir: {robot.direction}")
    robot.hull.print()
    return robot.panels_painted()

def solve(lines: Lines) -> int:
    """Solve the problem."""
    proc = IntCode(lines[0])
    robot = Robot(proc)
    robot.run()
    return robot.panels_painted()

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    proc = IntCode(lines[0])
    robot = Robot(proc)
    robot.hull.color(robot.loc, WHITE)
    robot.run()
    robot.hull.print()


# PART 1

def example1() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    result = test_robot()
    expected = 6
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    lines = load_input(INPUTFILE)
    result = solve(lines)
    print(f"result is {result}")
    assert result == 2088
    print("= " * 32)


# PART 2

def part2(lines: Lines) -> None:
    print("PART 2:")
    lines = load_input(INPUTFILE)
    result = solve2(lines)
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    part2(input_lines)
