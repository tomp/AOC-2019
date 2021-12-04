#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 13
#
import pdb
from typing import Sequence, Optional, Union, Any
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict, ChainMap
from location import Location, Delta


UNKNOWN = 0
EMPTY = 1
WALL = 2
DROID = 3
OXYGEN = 4

TILE = {
    UNKNOWN: " ",
    EMPTY: ".",
    WALL: "#",
    DROID: "D",
    OXYGEN: "x",
}

class Field:
    def __init__(self):
        self.tiles: dict[Location, int] = defaultdict(int)
        self.tile(Location(0, 0), EMPTY)
        self.droid = Location(0, 0)

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
        tiles = ChainMap({self.droid: DROID}, self.tiles)
        rows = []
        for r in range(rmin, rmax+1):
            row = []
            for c in range(cmin, cmax+1):
                row.append(TILE[tiles[Location(r, c)]])
            rows.append("".join(row))
        return "\n".join(rows)

