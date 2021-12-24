#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 16
#
from typing import Sequence, Any
from collections.abc import Iterable
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain, cycle, repeat, islice
from functools import cache, reduce
from operator import add
from math import ceil
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_CASES2 = [
    ("80871224585914546619083218645595", "24176176"),
    ("19617804207202209144916044189917", "73745418"),
    ("69317163492948606335995924319873", "52432133"),
]

SAMPLE_CASES2 = [
    ("80871224585914546619083218645595",
     "0070011050436210018092844731739021850250784875475759482496402895"),
]

SAMPLE_CASES = [
    ("80871224585914546619083218645595", "24176176"),
    ("19617804207202209144916044189917", "73745418"),
    ("69317163492948606335995924319873", "52432133"),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def sample_case(idx: int = 0) -> tuple[Lines, int]:
    text, expected = SAMPLE_CASES[idx]
    lines = load_text(text)
    return lines, expected

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

BASE = [0, 1, 0, -1]
BASE_SIZE = len(BASE)

# def pattern(size: int, idx: int = 0) -> list[int]:
#     values = cycle(chain(
#         repeat(BASE[0], idx + 1),
#         repeat(BASE[1], idx + 1),
#         repeat(BASE[2], idx + 1),
#         repeat(BASE[3], idx + 1))
#     )
#     return islice(values, 1, size+1)

def pattern(size: int, idx: int = 0) -> list[int]:
    patt = islice(cycle(chain(
        repeat(BASE[0], idx + 1),
        repeat(BASE[1], idx + 1),
        repeat(BASE[2], idx + 1),
        repeat(BASE[3], idx + 1))
    ), 1, size+1)
    return patt

def find_runs(seq: Iterable[int]):
    result = []
    pos = 0
    last, start = next(seq), pos
    for value in seq:
        pos += 1
        if value != last:
            if last:
                result.append((last, start, pos))
            last, start = value, pos
    if last:
        result.append((last, start, pos+1))
    return result

def runs1(size: int, idx: int = 0) -> list[tuple[int, int, int]]:
    seq = pattern(size, idx)
    result = []
    pos = 0
    last, start = next(seq), pos
    for value in seq:
        pos += 1
        if value != last:
            if last:
                result.append((last, start, pos))
            last, start = value, pos
    if last:
        result.append((last, start, pos+1))
    return result

def runs(size: int, idx: int = 0) -> list[tuple[int, int, int]]:
    result = []
    blocks = ceil((size - idx) / (4 * (idx + 1)))
    for j in range(blocks):
        start = idx + (4 * j * (idx + 1))
        if start < size:
            end = min(start + idx + 1, size)
            result.append((1, start, end))
        start = 2 + (idx * 3) + (4 * j * ( idx + 1))
        if start < size:
            end = min(start + idx + 1, size)
            result.append((-1, start, end))
    return result

def sumseq(inarr: list[int], size: int, start: int, end: int) -> int:
    n = len(inarr)
    assert size >= n
    block_start, block_end = start // n, (end - 1) // n
    if block_start == block_end:
        return sum(inarr[start % n: (end - 1) % n + 1])
    result = sum(inarr[start % n:]) + sum(inarr[:(end - 1) % n + 1])
    result += sum(inarr) * (block_end - block_start -1)
    return result


def phase(inarray: list[int]) -> list[int]:
    result = []
    size = len(inarray)
    for i in range(size):
        patt = pattern(size, i)
        element = reduce(add, (v * c for v, c in zip(cycle(inarray), patt)))
        print(f"{i:6d}: runs({size},{i}): {runs1(size, i)[:5]}")
        print(f"{i:6d}: runs({size},{i}): {runs(size, i)[:5]}")
        print(f"{i:6d}: {inarray[i]} -> {element:6d} -> {abs(element) % 10}")
        result.append(abs(element) % 10)
    return result

def phase2(inarray: list[int]) -> list[int]:
    result = []
    size = len(inarray)
    print(f"phase2:  size={size}")
    for i in range(size):
        patt = pattern(size, i)
        element = reduce(add, (v * c for v, c in zip(cycle(inarray), patt)))
        # print(f"{i:6d}: runs({size},{i}): {runs1(size, i)[:5]}")
        # print(f"{i:6d}: runs({size},{i}): {runs(size, i)[:5]}")
        print(f"{i:6d}: {inarray[i]} -> {element:6d} -> {abs(element) % 10}")
        result.append(abs(element) % 10)
    return result

def phase3(inarray: list[int]) -> list[int]:
    result = []
    size = len(inarray)
    for i in range(size):
        patt = pattern(size, i)
        element = 0
        for val, start, end in runs(size, i):
            if val == 1:
                element += sumseq(inarray, size, start, end)
            else:
                element -= sumseq(inarray, size, start, end)
        print(f"{i:6d}: {inarray[i]} -> {element:6d} -> {abs(element) % 10}")
        result.append(abs(element) % 10)
    return result

def solve2(text: str, phases: int = 2, reps: int = 10000) -> int:
    """Solve the problem."""
    arr = list(map(int, text)) * reps
    print(f"size: {len(arr)}")
    for step in range(phases):
        print(f"\nPhase {step+1}")
        arr = phase3(arr)
    return "".join(map(str, arr[:32] + arr[-32:]))

def solve(text: str, phases: int = 100) -> int:
    """Solve the problem."""
    arr = list(map(int, text))
    for step in range(phases):
        print(f"\nPhase {step+1}")
        arr = phase(arr)
    return "".join(map(str, arr[:8]))


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines[0])
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines[0])
    print(f"result is {result}")
    assert result == "19239468"
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines[0])
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines[0])
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    # part1(input_lines)
    example2()
    # part2(input_lines)
