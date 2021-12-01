#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 13
#
import pdb
from typing import Sequence, Optional, Union, Any
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
import time

from intcode import IntCode

INPUTFILE = "input.txt"

Lines = Sequence[str]

# Utility functions

def load_input(infile: str) -> Lines:
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

@dataclass(frozen=True)
class Delta:
    """A Delta instance represents the difference between two locations
    on a grid.  Internally, it's represented using (row, column) offsets.
    """
    dr: int
    dc: int

    def __str__(self) -> str:
        return f"delta({self.dr}, {self.dc})"

    def __add__(self, other: "Delta") -> "Delta":
        return Delta(self.dr + other.dr, self.dc + other.dc)

    def __sub__(self, other: "Delta") -> "Delta":
        return Delta(self.dr - other.dr, self.dc - other.dc)


@dataclass(frozen=True)
class Location:
    """A Location instance represents a location on a grid.
    Internally, it's represented using (row, column) coordinates
    """
    r: int
    c: int

    def __str__(self) -> str:
        return f"({self.r}, {self.c})"

    def right(self) -> "Location":
        return Location(self.r, self.c + 1)

    def left(self) -> "Location":
        return Location(self.r, self.c - 1)

    def up(self) -> "Location":
        return Location(self.r - 1, self.c)

    def down(self) -> "Location":
        return Location(self.r + 1, self.c)

    def __add__(self, delta: Delta) -> "Location":
        return Location(self.r + delta.dr, self.c + delta.dc)

    def __sub__(self, other: "Location") -> Delta:
        return Delta(self.r - other.r, self.c - other.c)


EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

TILE = {
    EMPTY: " ",
    WALL: "@",
    BLOCK: "#",
    PADDLE: "_",
    BALL: "o",
}

SCORE_UPDATE = Location(0, -1)

RIGHT = 1
CENTER = 0
LEFT = -1


class Screen:
    def __init__(self):
        self.tiles: dict[Location, int] = defaultdict(int)
        self.tile(Location(0, 0), EMPTY)

    def tile(
        self, loc: Location, new_tile: Optional[int] = None
    ) -> int:
        """Get (or set) the tile at the specified location."""
        try:
            assert loc.r is not None and loc.c is not None
            if new_tile is not None:
                assert new_tile in TILE
                self.tiles[loc] = new_tile
            return self.tiles[loc]
        except Exception as exc:
            print(exc)
            pdb.set_trace()

    def bounds(self) -> tuple[int, int, int, int]:
        if not self.tiles:
            return 0, 0, 0, 0
        rmin = min([loc.r for loc in self.tiles.keys()])
        rmax = max([loc.r for loc in self.tiles.keys()])
        cmin = min([loc.c for loc in self.tiles.keys()])
        cmax = max([loc.c for loc in self.tiles.keys()])
        return rmin, rmax, cmin, cmax

    def dimensions(self) -> tuple[int, int]:
        rmin, rmax, cmin, cmax = self.bounds()
        return rmax - rmin + 1, cmax - cmin + 1

    def __str__(self):
        rmin, rmax, cmin, cmax = self.bounds()
        rows = []
        for r in range(rmin, rmax+1):
            row = []
            for c in range(cmin, cmax+1):
                row.append(TILE[self.tiles[Location(r, c)]])
            rows.append("".join(row))
        return "\n".join(rows)

    def count_blocks(self) -> int:
        return len([v for v in self.tiles.values() if v == BLOCK])


class Arcade:

    def __init__(self, proc: IntCode):
        self.screen: Screen = Screen()
        self.proc: IntCode = proc
        self.score: int = 0
        self.joystick: int = CENTER
        self._ball: Optional[Location] = None
        self._dball: Optional[Location] = None
        self._next_ball: Optional[Location] = None
        self.paddle: Optional[Location] = None
        self._next_paddle: Optional[Location] = None

    def run(self) -> bool:
        self.proc.input(self.joystick)
        done = self.proc.run()
        while True:
            # consume all output from last run
            tile: Optional[int] = 0
            while tile is not None:
                x = self.proc.output()
                y = self.proc.output()
                loc = Location(y, x)
                tile = self.proc.output()
                if loc == SCORE_UPDATE:
                    self.score = tile
                elif tile is not None:
                    self.screen.tile(loc, tile)
                    if tile == BALL:
                        # print(f"ball -> {str(loc)}")
                        self.ball(loc)
                    elif tile == PADDLE:
                        # print(f"paddle -> {str(loc)}")
                        self.paddle = loc
            if done:
                break

            self.update_joystick()
            # Display the arcade screen
            print(f"SCORE: {self.score}")
            # print(f"ball:   {str(self._ball)} -> {str(self._next_ball)}")
            # print(f"paddle: {str(self.paddle)} -> {str(self._next_paddle)}")
            print(str(self.screen))
            time.sleep(0.1)
            self.proc.input(self.joystick)
            done = self.proc.run()
        return done

    def ball(self, new_loc: Optional[Location] = None) -> Optional[Location]:
        if new_loc:
            if self._ball:
                # if self._next_ball:
                #     print(f"ball: {str(self._ball)} -> {str(new_loc)} ({str(self._next_ball)})")
                #     assert new_loc == self._next_ball
                self._dball =  new_loc - self._ball
                # print(f"ball direction is {str(self._dball)}")
            self._ball = new_loc
        return self._ball

    def update_joystick(self) -> None:
        if not self.paddle or not self._ball or not self._dball:
            self.joystick = CENTER
            self._next_ball = None
            return

        ball, dloc = self._ball, self._dball
        next_ball = ball + dloc
        paddle = self.paddle
        contact = next_ball.r == paddle.r

        # Ball is about to bounce off a side wall
        if self.screen.tile(ball.right()) in (BLOCK, WALL) and dloc.dc == 1:
            dloc = Delta(dloc.dr, -1)
        elif self.screen.tile(ball.left()) in (BLOCK, WALL) and dloc.dc == -1:
            dloc = Delta(dloc.dr, 1)

        # ball is about to hit a block or wall, above
        if dloc.dr == -1:
            if self.screen.tile(ball.up()) in (BLOCK, WALL):
                dloc = Delta(1, dloc.dc)
            elif self.screen.tile(ball + dloc) == BLOCK:
                dloc = Delta(1, -dloc.dc)

        # block is about to hit a block or paddle, below
        else:
            if self.screen.tile(ball.down()) == BLOCK:
                dloc = Delta(-1, dloc.dc)
            elif self.screen.tile(next_ball) == BLOCK:
                dloc = Delta(-1, -dloc.dc)
            
        if contact:
            if ball.c == paddle.c:
                dloc = Delta(-1, dloc.dc)
                self.joystick = CENTER
            elif next_ball.c == paddle.c:
                dloc = Delta(-1, -dloc.dc)
                self.joystick = CENTER
            elif next_ball.c < paddle.c:
                dloc = Delta(-1, dloc.dc)
                self.joystick = LEFT
            elif next_ball.c > paddle.c:
                dloc = Delta(-1, dloc.dc)
                self.joystick = RIGHT
        else:
            if paddle.c < next_ball.c:
                self.joystick = RIGHT
            elif paddle.c > next_ball.c:
                self.joystick = LEFT
            else:
                self.joystick = CENTER

        # print(f"ball direction: {str(self._dball)} -> {str(dloc)}")

        self._next_ball = ball + dloc
        # print(f"ball prediction {str(self._next_ball)}")

        self._next_paddle = self.paddle + Delta(0, self.joystick)
        # print(f"joystick: {self.joystick}")


    def count_blocks(self) -> int:
        return self.screen.count_blocks()


class MockIntCode:
    """A MockIntCode simulates a regular IntCode processor, for testing.
    The client is expected to execute the run() method, and then read
    any values on the output stream.  The supplied out list is a list
    of lists - every time the processor is run(), the next set of output
    values is provided.
    """
    def __init__(self, inp: list[int], out: list[list[int]]):
        self.inp = inp
        self.out = [[]] + out

    def input(self, value: int) -> None:
        pass

    def run(self) -> bool:
        """Simulate running the processor.  True ("done") is returned
        when there are no more output values to produce.
        """
        if self.out:
            self.out = self.out[1:]
        return not self.out

    def output(self):
        """Return the next output value.  Returns None if there are no
        more values in the output queue.
        """
        if self.out and self.out[0]:
            return self.out[0].pop(0)
        return None


def test_arcade() -> None:
    proc = MockIntCode(
        inp=[], 
        out=[[1, 2, 3, 6, 5, 4]])
    arcade = Arcade(proc)
    arcade.run()
    print(str(arcade.screen))
    return arcade.count_blocks()

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    proc = IntCode(lines[0])
    proc.mem[0] = 2
    arcade = Arcade(proc)
    arcade.run()
    return arcade.score

def solve(lines: Lines) -> int:
    """Solve the problem."""
    proc = IntCode(lines[0])
    arcade = Arcade(proc)
    arcade.run()
    print(f"SCORE: {arcade.score}")
    print(str(arcade.screen))
    return arcade.count_blocks()


# PART 1

def example1() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    test_arcade()
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 348
    print("= " * 32)


# PART 2

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 16999
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    part2(input_lines)
