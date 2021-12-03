#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 14
#
from typing import Sequence, Any
from collections import defaultdict
from dataclasses import dataclass
import math
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (   """
        9 ORE => 2 A
        8 ORE => 3 B
        7 ORE => 5 C
        3 A, 4 B => 1 AB
        5 B, 7 C => 1 BC
        4 C, 1 A => 1 CA
        2 AB, 3 BC, 4 CA => 1 FUEL
        """,
        165
    ),
    (   """
        157 ORE => 5 NZVS
        165 ORE => 6 DCFZ
        44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
        12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
        179 ORE => 7 PSHF
        177 ORE => 5 HKGWZ
        7 DCFZ, 7 PSHF => 2 XJWVT
        165 ORE => 2 GPVTF
        3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
        """,
        13312
    ),
    (   """
        2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
        17 NVRVD, 3 JNWZP => 8 VPVL
        53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
        22 VJHF, 37 MNCFX => 5 FWMGM
        139 ORE => 4 NVRVD
        144 ORE => 7 JNWZP
        5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
        5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
        145 ORE => 6 MNCFX
        1 NVRVD => 8 CXFTF
        1 VJHF, 6 MNCFX => 4 RFSQX
        176 ORE => 6 VJHF
        """,
        180697
    ),
    (   """
        171 ORE => 8 CNZTR
        7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
        114 ORE => 4 BHXH
        14 VRPVC => 6 BMBT
        6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
        6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
        15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
        13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
        5 BMBT => 4 WPTQ
        189 ORE => 9 KTJDG
        1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
        12 VRPVC, 27 CNZTR => 2 XDBXC
        15 KTJDG, 12 BHXH => 5 XCVML
        3 BHXH, 2 VRPVC => 7 MZWV
        121 ORE => 7 VRPVC
        7 XCVML => 6 RJRHP
        5 BHXH, 4 VRPVC => 5 LTCX
        """,
        2210736
    ),
]


SAMPLE_CASES2 = [
    (   """
        157 ORE => 5 NZVS
        165 ORE => 6 DCFZ
        44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
        12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
        179 ORE => 7 PSHF
        177 ORE => 5 HKGWZ
        7 DCFZ, 7 PSHF => 2 XJWVT
        165 ORE => 2 GPVTF
        3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
        """,
        82892753
    ),
    (   """
        2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
        17 NVRVD, 3 JNWZP => 8 VPVL
        53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
        22 VJHF, 37 MNCFX => 5 FWMGM
        139 ORE => 4 NVRVD
        144 ORE => 7 JNWZP
        5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
        5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
        145 ORE => 6 MNCFX
        1 NVRVD => 8 CXFTF
        1 VJHF, 6 MNCFX => 4 RFSQX
        176 ORE => 6 VJHF
        """,
        5586022
    ),
    (   """
        171 ORE => 8 CNZTR
        7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
        114 ORE => 4 BHXH
        14 VRPVC => 6 BMBT
        6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
        6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
        15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
        13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
        5 BMBT => 4 WPTQ
        189 ORE => 9 KTJDG
        1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
        12 VRPVC, 27 CNZTR => 2 XDBXC
        15 KTJDG, 12 BHXH => 5 XCVML
        3 BHXH, 2 VRPVC => 7 MZWV
        121 ORE => 7 VRPVC
        7 XCVML => 6 RJRHP
        5 BHXH, 4 VRPVC => 5 LTCX
        """,
        460664
    ),
]

Lines = Sequence[str]

# Utility functions

## Use these if blank lines should be discarded.
def sample_input() -> Lines:
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))

def load_input(infile: str) -> Lines:
    return filter_blank_lines(Path(infile).open())

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


# Solution

FORMULAS: dict[str, "Formula"] = {}

@dataclass
class Formula:
    """ A Formula represents how to create a given chemical product from
    a set of reactants.
    """
    def __init__(self, product: str, quantity: int, reactants: dict[str, int]):
        self.product = product
        self.quantity = quantity
        self.reactants = reactants
        self._level = 0 if product == "ORE" else -1
        FORMULAS[product] = self

    def __str__(self) -> str:
        inputs = ", ".join([f"{v} {k}" for k, v in self.reactants.items()])
        output = f"{self.quantity} {self.product}({self.level})"
        return f"{inputs} => {output}"

    @property
    def level(self) -> int:
        """Return the production level of this product.  This is calculated
        recursively from the levels of the reactants, if necessary.
        Returns None if the level can't yet be determined (because some
        formulas are still missing.)
        """
        if self._level < 0:
            try:
                self._level = 1 + max([FORMULAS[v].level for v in self.reactants])
            except KeyError:
                pass
        return self._level


def parse_input(lines) -> dict[str, dict[str, int]]:
    global FORMULAS
    FORMULAS = {}
    for line in lines:
        parts, product = line.split("=>")
        prod_count, prod_name = [v.strip() for v in product.split()]
        reactants = {}
        for item in parts.split(","):
            count, name = [v.strip() for v in item.split()]
            reactants[name] = int(count)
        assert prod_name not in FORMULAS
        FORMULAS[prod_name] = Formula(prod_name, int(prod_count), reactants)

    FORMULAS["ORE"] = Formula("ORE", 1, None)


def ore_needed(fuel: int) -> int:
    """Solve the problem."""
    need = {"FUEL": fuel}
    ore = 0
    while need:
        level = max([FORMULAS[v].level for v in need])
        chems = [name for name in need if FORMULAS[name].level == level]
        for chem in chems:
            amount_needed = need[chem]
            amount_per_formula = FORMULAS[chem].quantity
            formulas_needed = math.ceil(amount_needed / amount_per_formula)
            for k, v in FORMULAS[chem].reactants.items():
                if k == "ORE":
                    ore += v * formulas_needed
                elif k not in need:
                    need[k] = v * formulas_needed
                else:
                    need[k] += v * formulas_needed
            need[chem] = 0
        need = {k: v for k, v in need.items() if v > 0}
    return ore

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    parse_input(lines)
    total_ore = 1000000000000
    ore_per_fuel = ore_needed(1)
    fuel = total_ore // ore_per_fuel
    additional = (total_ore - ore_needed(fuel)) // ore_per_fuel
    while additional:
        fuel += additional
        additional = (total_ore - ore_needed(fuel)) // ore_per_fuel
    return fuel

def solve(lines: Lines) -> int:
    """Solve the problem."""
    parse_input(lines)
    return ore_needed(1)


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for arg, expected in SAMPLE_CASES:
        lines = load_text(arg)
        result = solve(lines)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 612880
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for arg, expected in SAMPLE_CASES2:
        lines = load_text(arg)
        result = solve2(lines)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 2509120
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
