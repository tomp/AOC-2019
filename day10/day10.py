#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 10
#
from typing import Union, Sequence, Text, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math

## Types
Lines = Sequence[str]
Matrix = Sequence[Sequence[Any]]

## Constants
INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        .#..#
        .....
        #####
        ....#
        ...##
        """,
        (8, 4, 3)
    ),
    (
        """
        ......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####
        """,
        (33, 8, 5)
    ),
    (
        """
        #.#...#.#.
        .###....#.
        .#....#...
        ##.#.#.#.#
        ....#.#.#.
        .##..###.#
        ..#...##..
        ..##....##
        ......#...
        .####.###.
        """,
        (35, 2, 1)
    ),
    (
        """
        .#..#..###
        ####.###.#
        ....###.#.
        ..###.##.#
        ##.##.#.#.
        ....###..#
        ..#.#..#.#
        #..#.#.###
        .##...##.#
        .....#.#..
        """,
        (41, 3, 6)
    ),
    (
        """
        .#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##
        """,
        (210, 13, 11)
    ),
]

SAMPLE_INPUT2 = """
        .#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##
"""

EXPECTED2 = [
    (1, 12, 11),
    (2, 1, 12),
    (3, 2, 12),
    (10, 8, 12),
    (20, 0, 16),
    (50, 9, 16),
    (100, 16, 10),
    (199, 6, 9),
    (200, 2, 8),
    (201, 9, 10),
    (299, 1, 11)
]

# Utility functions

def load_input(infile: str) -> Lines:
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

@dataclass(eq=True)
class Bearing:

    dr: int
    dc: int

    def __init__(self, dr: int, dc: int):
        self.dr = dr
        self.dc = dc
        self._normalize()

    def __hash__(self) -> int:
        return hash((self.dr, self.dc))

    def angle(self) -> float :
        """Express this bearing as a clockwwise angle (deg) from vertical."""
        result = math.atan2(self.dc, -self.dr) * 180.0 / math.pi
        if result < 0:
            result += 360
        return result

    def _normalize(self):
        if self.dr == 0:
            if self.dc > 0:
                self.dc = 1
            elif self.dc < 0:
                self.dc = -1
        elif self.dc == 0:
            if self.dr > 0:
                self.dr = 1
            else:
                self.dr = -1
        else:
            d = math.gcd(self.dr, self.dc)
            self.dr = self.dr // d
            self.dc = self.dc // d


@dataclass(order=True, frozen=True)
class Coord:
    r: int
    c: int

    def __str__(self):
        return f"({self.r}, {self.c})"

    def dist(self, other: "Coord") -> float:
        """Return the distance from this point to the other point."""
        dr, dc = other.r - self.r, other.c - self.c
        return math.sqrt(dr * dr + dc * dc)

    def bearing(self, other: "Coord") -> Bearing:
        """Return the bearing from this point to the other point."""
        return Bearing(other.r - self.r, other.c - self.c)


class Grid:
    """A Grid instance represents an asteroid map, where the object
    occupying every point in the grid is explicitly specified.  Methods are
    provided to get the asteroid locations and other derived quantities.
    """
    ASTEROID = "#"
    SPACE = "."

    def __init__(self, rows: Matrix):
        self.rows: Matrix = rows
        assert all([len(row) == len(rows[0]) for row in self.rows])

        self.nrow: int = len(rows)
        self.ncol: int = len(rows[0])
        self.asteroids: list[Coord] = self._locate_asteroids()

    def print(self) -> None:
        for row in self.rows:
            print("".join([str(item) for item in row]))

    def _locate_asteroids(self) -> list[Coord]:
        bodies = []
        for r in range(self.nrow):
            for c in range(self.ncol):
                if self.rows[r][c] == self.ASTEROID:
                    bodies.append(Coord(r, c))
        bodies.sort()
        return bodies

    def count_visible(self, rc0: Coord) -> int:
        count = defaultdict(int)
        for rc in self.asteroids:
            if rc == rc0:
                continue
            count[rc0.bearing(rc)] += 1
        return len(count)

    def monitoring_location(self) -> Coord:
        max_visible, rcf = 0, None
        for rc0 in self.asteroids:
            visible = self.count_visible(rc0)
            if visible > max_visible:
                max_visible, rcf = visible, rc0
        return rcf

    def vaporization_sequence(self, rc0: Coord) -> list[Coord]:
        bearing = defaultdict(list)
        for rc in self.asteroids:
            if rc == rc0:
                continue
            bearing[rc0.bearing(rc).angle()].append((rc0.dist(rc), rc))
        for bodies in bearing.values():
            bodies.sort()
            
        result = []
        while True:
            vaporized = 0
            for angle, bodies in sorted(bearing.items()):
                if bodies:
                    _, rc = bodies.pop(0)
                    result.append(rc)
                    vaporized += 1
            if not vaporized:
                break
        return result


def parse_input(text: Union[Lines, Text]) -> Grid:
    if isinstance(text, str):
        rows = filter_blank_lines(text.split("\n"))
    else:
        rows = filter_blank_lines(text)
    return Grid(rows)

def solve2(lines: Lines) -> tuple[int, int]:
    """Solve the problem."""
    grid = parse_input(lines)
    grid.print()
    rc0 = grid.monitoring_location()
    coords = grid.vaporization_sequence(rc0)
    rc = coords[199]
    return rc.c, rc.r

def solve(lines: Lines) -> int:
    """Solve the problem."""
    grid = parse_input(lines)
    grid.print()
    rc0 = grid.monitoring_location()
    return grid.count_visible(rc0)


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for arg, expected in SAMPLE_CASES:
        grid = parse_input(arg)
        rc0 = grid.monitoring_location()
        visible = grid.count_visible(rc0)
        result = (visible, rc0.r, rc0.c)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 247
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    grid = parse_input(SAMPLE_INPUT2)
    rc0 = grid.monitoring_location()
    result = grid.vaporization_sequence(rc0)
    for idx, ri, ci in EXPECTED2:
        rc = result[idx-1]
        print(f"'The {idx}th asteroid to be vaporized is at {rc.r, rc.c} (expected {(ri, ci)})")
        assert (rc.r, rc.c) == (ri, ci)
    print("= " * 32)

def part2(lines: Lines) -> None:
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
