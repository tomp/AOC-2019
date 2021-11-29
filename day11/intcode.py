#!/usr/bin/env python3
"""
Intcode processor simulator
"""
from typing import Optional, Union
from collections import defaultdict
from copy import copy


ADDR_POSITION, ADDR_IMMEDIATE, ADDR_RELATIVE = "0", "1", "2"

class IntCode:
    """An IntCode instance represents a unique intcode processor.
    The processor runs in asynchronous style, running until it exits
    normally, or needs to wait for input to become available.
    Each processor has its own input and output streams (lists).
    """

    def __init__(self, mem: Union[str, list[int]]):
        self.mem = defaultdict(int)
        self.inp = [] # input stream
        self.out = [] # output stream
        self.loc = 0 # instruction pointer
        self.base = 0 # relative base
        self.done = False # True, once exit instruction is executed

        if isinstance(mem, list):
            for i, v in enumerate(mem):
                self.mem[i] = v
        elif isinstance(mem, str):
            for i, v in enumerate(mem.split(",")):
                self.mem[i] = int(v.strip())
        # print("#### new IntCode")
        # print(f"{self.to_str()}")

    def input(self, value: int):
        self.inp.append(value)

    def output(self) -> int:
        if self.out:
            return self.out.pop(0)
        return None

    def run(self) -> bool:
        """Continue execution of the intcode program from the current
        instruction pointer.  Execution will continue until an exit
        instruction is found or we're blocked by input.
        """
        op, addr = parse_instruction(self.mem[self.loc])
        while True:
            # print(
            #     f"[{self.loc:02d}] '{self.mem[self.loc]}': op {op} mode {addr} "
            #     f"...{self.to_str(self.loc, self.loc+4)} ..."
            # )
            if op == "01":
                a, b, c = self.mem[self.loc + 1], self.mem[self.loc + 2], self.mem[self.loc + 3]
                va = self.parameter_value(a, addr[0])
                vb = self.parameter_value(b, addr[1])
                self.store(va + vb, c, addr[2])
                self.loc += 4
            elif op == "02":
                a, b, c = self.mem[self.loc + 1], self.mem[self.loc + 2], self.mem[self.loc + 3]
                va = self.parameter_value(a, addr[0])
                vb = self.parameter_value(b, addr[1])
                self.store(va * vb, c, addr[2])
                self.loc += 4
            elif op == "03":
                if not self.inp:
                    break
                a = self.mem[self.loc + 1]
                self.store(self.inp.pop(0), a, addr[0])
                # print(f"self.mem[{a}] <-- input {self.mem[a]}")
                self.loc += 2
            elif op == "04":
                a = self.mem[self.loc + 1]
                va = self.parameter_value(a, addr[0])
                self.out.append(va)
                # print(f"self.mem[{a}] --> output {self.mem[a]}")
                self.loc += 2
            elif op == "05":
                a, b = self.mem[self.loc + 1], self.mem[self.loc + 2]
                va = self.parameter_value(a, addr[0])
                vb = self.parameter_value(b, addr[1])
                if va:
                    self.loc = vb
                else:
                    self.loc += 3
            elif op == "06":
                a, b = self.mem[self.loc + 1], self.mem[self.loc + 2]
                va = self.parameter_value(a, addr[0])
                vb = self.parameter_value(b, addr[1])
                if not va:
                    self.loc = vb
                else:
                    self.loc += 3
            elif op == "07":
                a, b, c = self.mem[self.loc + 1], self.mem[self.loc + 2], self.mem[self.loc + 3]
                va = self.parameter_value(a, addr[0])
                vb = self.parameter_value(b, addr[1])
                if va < vb:
                    self.store(1, c, addr[2])
                else:
                    self.store(0, c, addr[2])
                self.loc += 4
            elif op == "08":
                a, b, c = self.mem[self.loc + 1], self.mem[self.loc + 2], self.mem[self.loc + 3]
                va = self.parameter_value(a, addr[0])
                vb = self.parameter_value(b, addr[1])
                if va == vb:
                    self.store(1, c, addr[2])
                else:
                    self.store(0, c, addr[2])
                self.loc += 4
            elif op == "09":
                a = self.mem[self.loc + 1]
                va = self.parameter_value(a, addr[0])
                self.base += va
                self.loc += 2
            elif op == "99":
                self.done = True
                break
            else:
                raise RuntimeError(f"unrecognized op '{op}'")
            op, addr = parse_instruction(self.mem[self.loc])

        # print(f"---- {','.join([str(v) for v in self.mem])}")
        return self.done

    def parameter_value(self, param: int, addr_mode: int) -> int:
        if addr_mode == ADDR_POSITION: # position mode
            return self.mem[param]
        if addr_mode == ADDR_IMMEDIATE: # immediate mode
            return param
        if addr_mode == ADDR_RELATIVE: # relative mode
            return self.mem[self.base + param]

    def store(self, value: int, param: int, addr_mode: int):
        if addr_mode == ADDR_POSITION: # position mode
            self.mem[param] = value
        elif addr_mode == ADDR_IMMEDIATE: # immediate mode
            raise ValueError("immediate mode for assignment address")
        elif addr_mode == ADDR_RELATIVE: # relative mode
            self.mem[self.base + param] = value

    def to_str(self, start: int = 0, end: int = 0):
        """Return a string representation of the memory locations from start
        to end (non-inclusive).
        """
        if end == 0:
            end = max(self.mem.keys()) + 1
        return ", ".join([str(self.mem[v]) for v in range(start, end)])


def parse_instruction(value: int) -> tuple[str, tuple[bool]]:
    """Parse out the opcode and the address modes for the parameters of the
    given integer instruction.  A tuple of the opcode (str) and the three
    address modes (int) is returned.
    """
    digits = f"{value:05d}"
    op = digits[3:]
    addr_mode = (digits[2], digits[1], digits[0])
    return op, addr_mode


def init_mem(
        line: str,
        noun: int = None,
        verb: int = None,
        size: int = None
) -> list[int]:
    """Create an initial memory image from the given, single-line string
    repreentation of an intcode program.
    """
    mem = [int(v.strip()) for v in line.split(",")]
    if noun is not None:
        mem[1] = noun
    if verb is not None:
        mem[2] = verb
    if size is not None and len(mem) < size:
        mem += [0] * (size - len(mem))
    return mem


def test_engine():
    """Run some basic tests to make sure the intcode engine runs as
    expected.  An exception is raised if there's any error.
    """
    # example from day 5 part 1 description
    proc = IntCode("1002,4,3,4,33")
    ok = proc.run()
    assert ok
    assert proc.mem[proc.loc] == 99

    # addition of address mode parameters
    proc = IntCode("1,5,6,7,99,8,13,0")
    ok = proc.run()
    assert ok
    assert proc.mem[7] == 21

    # multiplication of address mode parameters
    proc = IntCode("2,5,6,7,99,8,13,0")
    ok = proc.run()
    assert ok
    assert proc.mem[7] == 104

    # addition of immediate mode and address mode parameters
    proc = IntCode("101,4,6,7,99,8,13,0")
    ok = proc.run()
    assert ok
    assert proc.mem[7] == 17

    # multiplication of address mode and immediate mode parameters
    proc = IntCode("1002,5,9,7,99,8,13,0")
    ok = proc.run()
    assert ok
    assert proc.mem[7] == 72

    # multiplication of values read from input
    proc = IntCode("3,15,3,16,2,15,16,17,4,17,99")
    proc.input(3)
    proc.input(17)
    ok = proc.run()
    assert ok
    assert proc.mem[17] == 51
    assert proc.output() == 51

    # multiplication of values read from input to relative locations
    proc = IntCode("109,20,203,10,203,11,22202,10,11,12,204,12,99")
    proc.input(3)
    proc.input(17)
    ok = proc.run()
    assert ok
    assert proc.base == 20
    assert proc.mem[32] == 51
    assert proc.output() == 51

if __name__ == '__main__':
    test_engine()
    print("all tests passed")
