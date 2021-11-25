#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 8
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
123456712012
"""

SAMPLE_INPUT2 = """
0222112222120000
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

def print_layer(pixels: str, width: int, height: int):
    """Print the layer."""
    PIX = {"0": " ", "1": "#"}
    display = "".join([PIX[v] for v in pixels])
    print("\n".join([display[v*width:(v+1)*width] for v in range(height)]))

def get_layers(text: str, width: int, height: int) -> list[str]:
    """Split the input text into layers of size width * height."""
    npix = len(text.strip())
    size = width * height
    assert npix % size == 0
    return [text[v*size:(v+1)*size] for v in range(npix // size)]

def top_pixel(pixels: list[str]) -> str:
    for pixel in pixels:
        if pixel != "2":
            return pixel
    return "2"

def solve2(text: str, width: int, height: int) -> str:
    """Solve the problem."""
    layers = get_layers(text, width, height)
    pixels = "".join([top_pixel(p) for p in zip(*layers)])
    print_layer(pixels, width, height)
    return pixels

def solve(text: str, width: int, height: int) -> int:
    """Solve the problem."""
    layers = get_layers(text, width, height)
    size = width * height
    minZeros = size
    target = ""
    for layer in layers:
        nZeros = layer.count("0")
        if nZeros < minZeros:
            minZeros = nZeros
            target = layer
    nOnes = target.count("1")
    nTwos = target.count("2")
    return nOnes * nTwos


# PART 1

def example1():
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve(lines[0], 3, 2)
    expected = 1
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    print("PART 1:")
    result = solve(lines[0], 25, 6)
    print(f"result is {result}")
    assert result == 1330
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input lines."""
    print("EXAMPLE 2:")
    lines = filter_blank_lines(SAMPLE_INPUT2.split("\n"))
    result = solve2(lines[0], 2, 2)
    expected = "0110"
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part2(lines):
    print("PART 1:")
    result = solve2(lines[0], 25, 6)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
