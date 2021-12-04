#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 13
#
from typing import Sequence, Optional, Union, Any
import time

from intcode import IntCode
from location import Location, Delta
from field import Field, UNKNOWN, EMPTY, WALL, OXYGEN


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

TURN_RIGHT = {
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST,
    WEST: NORTH,
}

TURN_LEFT = {
    NORTH: WEST,
    EAST: NORTH,
    SOUTH: EAST,
    WEST: SOUTH,
}

TURN_BACK = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}

DIR = {
    NORTH: "north",
    EAST: "east",
    SOUTH: "south",
    WEST: "west",
}

MOVE = {
    NORTH: Delta(-1, 0),
    EAST: Delta(0, 1),
    SOUTH: Delta(1, 0),
    WEST: Delta(0, -1),
}

BLOCKED = 0
OK = 1
EUREKA = 2

class Droid:

    def __init__(self, proc: IntCode):
        self.field: Field = Field()
        self.proc: IntCode = proc
        self.loc: Location = Location(0, 0)
        self.oxygen: Optional[Location]  = None
        self.last_move: int = NORTH
        self.explored: set[Location] = set()

    def step(self, move: int, complete_map: bool = False) -> bool:
        """Move one step in the move direction.  The map and our location
        are updated, based on the response.  Return True if we found the
        oxygen generator, else False.
        """
        next_loc = self.loc + MOVE[move]
        self.last_move = move
        self.proc.input(move)
        _ = self.proc.run()
        response = self.proc.output()
        if response == BLOCKED:
            self.field.tile(next_loc, WALL)
            done = False
        elif response == OK:
            self.field.tile(next_loc, EMPTY)
            self.loc = next_loc
            self.field.droid = self.loc
            done = False
        elif response == EUREKA:
            self.oxygen = next_loc
            self.loc = next_loc
            if not complete_map:
                self.field.tile(next_loc, OXYGEN)
                done = True
            else:
                self.field.tile(next_loc, EMPTY)
                done = False
        return done

    def run(self, complete_map: bool = False) -> bool:
        done = False
        while not done:
            move = self.next_move()
            if move:
                done = self.step(move, complete_map)
            else:
                done = True
            print("----------------")
            print(str(self.field))
            # time.sleep(0.1)
        return done

    def next_move(self) -> int:
        """Choose next move, following keep-righthand-on-the-wall strategy.
        """
        move = self.last_move
        fwd_loc = self.loc + MOVE[move]
        fwd_tile = self.field.tile(fwd_loc)
        fwd_blocked = (fwd_tile == WALL or fwd_loc in self.explored)

        right_loc = self.loc + MOVE[TURN_RIGHT[move]]
        right_tile = self.field.tile(right_loc)
        right_blocked = (right_tile == WALL or right_loc in self.explored)

        left_loc = self.loc + MOVE[TURN_LEFT[move]]
        left_tile = self.field.tile(left_loc)
        left_blocked = (left_tile == WALL or left_loc in self.explored)

        back_loc = self.loc + MOVE[TURN_BACK[move]]
        back_tile = self.field.tile(back_loc)
        back_blocked = (back_tile == WALL or back_loc in self.explored)

        if fwd_tile == UNKNOWN:
            return move
        if right_tile == UNKNOWN:
            return TURN_RIGHT[move]
        if left_tile == UNKNOWN:
            return TURN_LEFT[move]
        if back_tile == UNKNOWN:
            return TURN_BACK[move]

        if fwd_tile == EMPTY and not fwd_blocked:
            if back_blocked and right_blocked and left_blocked:
                self.explored.add(self.loc)
            if right_blocked:
                # continue forward until we find a wall
                return move
            if right_tile == EMPTY:
                # turn right if we get to a corner
                return TURN_RIGHT[move]
            # continue forward until we find a wall
            return move

        if fwd_blocked:
            if right_tile == EMPTY and not right_blocked:
                # turn left, to put wall on our right side
                if left_blocked and back_blocked:
                    self.explored.add(self.loc)
                return TURN_RIGHT[move]
            if left_tile == EMPTY and not left_blocked:
                # turn left, to put wall on our right side
                if right_blocked and back_blocked:
                    self.explored.add(self.loc)
                return TURN_LEFT[move]
            if back_tile == EMPTY and not back_blocked:
                # turn back if we can't go left
                self.explored.add(self.loc)
                return TURN_BACK[move]

        return None
        # raise RuntimeError("No moves found at {self.loc}")

    def neighbors(self, loc: Location) -> list[Location]:
        result = []
        for move, delta in MOVE.items():
            next_loc = loc + delta
            tile = self.field.tile(next_loc)
            if tile == EMPTY or tile == OXYGEN:
                result.append(next_loc)
        return result

    def shortest_path(self) -> int:
        """Return length of shortest path from (0, 0) to the oxygen generator."""
        assert self.oxygen is not None

        # queue contains (loc, prev_loc, distance) tuples
        queue = [(Location(0, 0), None, 0)]
        last_dist = 0
        while queue:
            loc, last_loc, dist = queue.pop(0)
            assert dist >= last_dist
            if loc == self.oxygen:
                return dist

            for next_loc in self.neighbors(loc):
                if next_loc != last_loc:
                    queue.append((next_loc, loc, dist+1))
        return None

    def oxygen_fill_time(self) -> int:
        """Return number timeunits required to fill ship with oxygen."""
        assert self.oxygen is not None

        # queue contains (loc, prev_loc, distance) tuples
        queue = [(self.oxygen, None, 0)]
        last_dist = 0
        while queue:
            loc, last_loc, dist = queue.pop(0)
            assert dist >= last_dist

            for next_loc in self.neighbors(loc):
                if next_loc != last_loc:
                    queue.append((next_loc, loc, dist+1))
            last_dist = dist
        return last_dist


