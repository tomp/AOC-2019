#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 12
#
from typing import Sequence, Optional
from pathlib import Path
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        <x=-1, y=0, z=2>
        <x=2, y=-10, z=-7>
        <x=4, y=-8, z=8>
        <x=3, y=5, z=-1>
        """,
        10, 179
    ),
    (
        """
        <x=-8, y=-10, z=0>
        <x=5, y=5, z=10>
        <x=2, y=-7, z=3>
        <x=9, y=-8, z=-3>
        """,
        100, 1940
    ),
]

SAMPLE_CASES2 = [
    (
        """
        <x=-1, y=0, z=2>
        <x=2, y=-10, z=-7>
        <x=4, y=-8, z=8>
        <x=3, y=5, z=-1>
        """,
        2772
    ),
    (
        """
        <x=-8, y=-10, z=0>
        <x=5, y=5, z=10>
        <x=2, y=-7, z=3>
        <x=9, y=-8, z=-3>
        """,
        4686774924
    ),
]

Lines = Sequence[str]

VECTOR_RE = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")


# Utility functions

## Use these if blank lines should be discarded.
def sample_input(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def load_input(infile: str) -> Lines:
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


# Solution

@dataclass(frozen=True)
class Vector:
    x: int
    y: int
    z: int

    def __str__(self):
        return f"<x={self.x:3d}, y={self.y:3d}, z={self.z:3d}>"

    def energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def compare(self, other: "Vector") -> "Vector":
        return Vector(
            sign(self.x - other.x),
            sign(self.y - other.y),
            sign(self.z - other.z)
        )


class Body:
    """A Body represents the position and velocity of a single orbital body.
    """
    def __init__(self, position: Vector, velocity: Optional[Vector] = None):
        self.r = position
        if velocity is None:
            self.v = Vector(0, 0, 0)
        else:
            self.v = velocity
        self.history = [self.phase_state()]

    def __str__(self):
        return f"pos={str(self.r)}, vel={str(self.v)}"

    def total_energy(self) -> int:
        return self.r.energy() * self.v.energy()

    def step(self, force: Vector):
        self.v += force
        self.r += self.v
        self.history.append([self.phase_state()])

    def compare(self, other: "Body") -> Vector:
        return self.r.compare(other.r)

    def phase_state(self):
        return self.r.x, self.r.y, self.r.z, self.v.x, self.v.y, self.v.z


class OrbitalSystem:
    def __init__(self, bodies: list[Body]):
        self.bodies: list[Body] = bodies
        self.time: int = 0
        self.init: dict[str, Any] = self.xyz_state()
        self.period: dict[str, int] = {}
        self.cycle: Optional[int] = None

    def total_energy(self) -> int:
        return sum([body.total_energy() for body in self.bodies])

    def calculate_forces(self):
        result = []
        for body in self.bodies:
            forces = Vector(0, 0, 0)
            for other in self.bodies:
                if body is not other:
                    forces += other.compare(body)
            result.append(forces)
        return result

    def step(self):
        forces = self.calculate_forces()
        for body, force in zip(self.bodies, forces):
            body.step(force)
        self.time += 1

        state = self.xyz_state()
        if state['xr'] == self.init['xr'] and state['xv'] == self.init['xv']:
            if 'x' not in self.period:
                self.period["x"] = self.time 
                print(f"Period X: {self.period['x']}")
        if state['yr'] == self.init['yr'] and state['yv'] == self.init['yv']:
            if 'y' not in self.period:
                self.period["y"] = self.time
                print(f"Period Y: {self.period['y']}")
        if state['zr'] == self.init['zr'] and state['zv'] == self.init['zv']:
            if 'z' not in self.period:
                self.period["z"] = self.time
                print(f"Period Z: {self.period['z']}")

        if self.cycle is None:
            if len(self.period) == 3:
                self.cycle = lcm(self.period["x"], self.period["y"], self.period["z"])
                print(f"Cycle time: {self.cycle}")

    def xyz_state(self):
        xr, xv, yr, yv, zr, zv = [], [], [], [], [], []
        for b in self.bodies:
            xr.append(b.r.x)
            xv.append(b.v.x)
            yr.append(b.r.y)
            yv.append(b.v.y)
            zr.append(b.r.z)
            zv.append(b.v.z)
        return {'xr': xr, 'xv': xv, 'yr': yr, 'yv': yv, 'zr': zr, 'zv': zv}

    def print_state(self):
        print(f"After {self.time} steps:")
        for body in self.bodies:
            print(str(body))
        print(f"Total energy: {self.total_energy()}")

    def print_oneline_state(self):
        state = " : ".join([str(v.phase_state()) for v in self.bodies])
        print(f"{self.time}: {state}")

    def print_xyz_state(self, init=False):
        if init:
            time, state = 0, self.init
        else:
            time, state = self.time, self.xyz_state()
        print(f"{time}: {state['xr']}, {state['xv']} : {state['yr']}, {state['yv']} : {state['zr']}, {state['zv']}")


def lcm(*values: list[int]) -> int:
    args = list(values)
    result = args.pop(0)
    while args:
        arg = args.pop(0)
        result = result * arg //math.gcd(result, arg)
    return result

def sign(v: int) -> int:
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0

def parse_input(lines) -> list[Body]:
    result = []
    for line in lines:
        m = VECTOR_RE.match(line)
        if m:
            xyz = [int(v) for v in m.groups()]
            result.append(Body(Vector(*xyz)))
    return result


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    bodies = parse_input(lines)

    system = OrbitalSystem(bodies)
    system.print_state()
    # system.print_xyz_state()
    while system.cycle is None:
        system.step()
        # system.print_xyz_state()
    return system.cycle


def solve(lines: Lines, steps: int) -> int:
    """Solve the problem."""
    bodies = parse_input(lines)

    system = OrbitalSystem(bodies)
    # system.print_state()
    for step in range(steps):
        system.step()
        # system.print_state()
    return system.total_energy()


# PART 1

#!! DELETE THE example1 FUNCTION YOU'RE NOT GOING TO USE

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, steps, expected in SAMPLE_CASES:
        lines = sample_input(text)
        result = solve(lines, steps)
        print("\n".join(lines))
        print(f"'energy after {steps}' steps -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines, 1000)
    print(f"result is {result}")
    assert result == 7988
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = sample_input(text)
        result = solve2(lines)
        print(f"result is {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
