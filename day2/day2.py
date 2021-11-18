#!/usr/bin/env python3
#
#  Advent of Code 2019 - day 2
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    ("1,9,10,3,2,3,11,0,99,30,40,50", (0, 3500)),
    ("1,0,0,0,99", (0, 2)),
    ("2,3,0,3,99", (3, 6)),
    ("2,4,4,5,99,0", (5, 9801)),
    ("1,1,1,4,99,5,6,0,99", (0, 30)),
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

def run_intcode(code: list[int]) -> int:
    mem = list(code)
    loc = 0 # current position
    while mem[loc] != 99:
        # print(f"[{loc:02d}] {','.join([str(v) for v in mem])}") 
        if mem[loc] == 1:
            a, b, c = mem[loc+1:loc+4]
            mem[c] = mem[a] + mem[b]
            loc += 4
        elif mem[loc] == 2:
            a, b, c = mem[loc+1:loc+4]
            mem[c] = mem[a] * mem[b]
            loc += 4
        else:
            raise RuntimeError(f"unrecognized op '{mem[loc]}'")
    # print(f"---- {','.join([str(v) for v in mem])}") 
    return mem


def init_mem(line: str, noun: int = None, verb: int = None) -> list[int]:
    mem = [int(v) for v in line.split(",")]
    if noun is not None:
        mem[1] = noun
    if verb is not None:
        mem[2] = verb
    return mem


def solve(line: str, pos: int = 0, noun: int = None, verb: int = None) -> int:
    """Solve the problem."""
    mem = init_mem(line, noun, verb)
    mem = run_intcode(mem)
    return mem[pos]


def solve2(line: str, target: int) -> int:
    """Solve the problem."""
    size = line.count(",")
    for noun in range(size):
        for verb in range(size):
            mem = init_mem(line, noun, verb)
            mem = run_intcode(mem)
            # print(f"{noun}, {verb} -->  {mem[0]}")
            if mem[0] == target:
                return (100 * noun) + verb
    return None


# PART 1

#!! DELETE THE example1 FUNCTION YOU'RE NOT GOING TO USE

def example1():
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for arg, (pos, expected) in SAMPLE_CASES:
        result = solve(arg, pos=pos)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)


def part1(lines):
    print("PART 1:")
    result = solve(lines[0], noun=12, verb=2)
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def part2(lines):
    print("PART 1:")
    result = solve2(lines[0], target=19690720)
    print(f"result is {result}")
    print("= " * 32)




if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    # example2()
    part2(lines)
