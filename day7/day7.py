#!/usr/bin/env python3
#
#  Advent of Code 2019 - day 7
#
from pathlib import Path
from itertools import permutations
from copy import copy
from intcode import init_mem, IntCode

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", 43210),
    ("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
     54321,
    ),
    ("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,"
     "31,1,32,31,31,4,31,99,0,0,0",
     65210,
    ),
]

SAMPLE_CASES2 = [
    ("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
     "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
     139629729
    ),
    ("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,"
     "-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,"
     "53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
     18216
    )
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

def run_amplifiers2(mem: list[int], phases: list[int]) -> int:
    """Run five chained instances of the given intcode program (mem)
    using the given phase for each instance.  This version connects the
    last amplifier to the first, and runs until the last amplifier exits.
    The final output signal is returned.
    """
    amps = [IntCode(mem) for _ in range(5)]
    for amp, phase in zip(amps, phases):
        amp.input(phase)

    signal = 0
    done = False
    while not done:
        for amp in amps:
            amp.input(signal)
            done = amp.run()
            signal = amp.output()
    return signal

def solve2(line):
    """Solve the problem."""
    mem = init_mem(line)
    best_signal = 0
    best_phases = []
    for phases in permutations([5, 6, 7, 8, 9]):
        signal = run_amplifiers2(mem, phases)
        if signal > best_signal:
            best_signal = signal
            best_phases = ''.join([str(v) for v in phases])
    return best_signal

def run_amplifiers(mem: list[int], phases: list[int]) -> int:
    """Run five chained instances of the given intcode program (mem)
    using the given phase for each instance.  The integer output signal
    is returned.
    """
    amps = [IntCode(mem) for _ in range(5)]
    for amp, phase in zip(amps, phases):
        amp.input(phase)

    signal = 0
    for amp in amps:
        amp.input(signal)
        done = amp.run()
        signal = amp.output()
    return signal

def solve(line):
    """Solve the problem."""
    mem = init_mem(line)
    best_signal = 0
    best_phases = []
    for phases in permutations([0, 1, 2, 3, 4]):
        signal = run_amplifiers(mem, phases)
        if signal > best_signal:
            best_signal = signal
            best_phases = ''.join([str(v) for v in phases])
    return best_signal


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
    assert result == 117312
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
    result = solve2(lines[0])
    print(f"result is {result}")
    assert result == 1336480
    print("= " * 32)

if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
