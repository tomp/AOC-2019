#!/usr/bin/env python3
"""
Intcode processor simulator
"""
from typing import Optional
from copy import copy


class IntCode:
    """An IntCode instance represents a unique intcode processor.
    The processor runs in asynchronous style, running until it exits
    normally, or needs to wait for input to become available.
    Each processor has its own input and output streams (lists).
    """

    def __init__(self, mem: list[int]):
        self.mem = copy(mem) # memory image
        self.inp = [] # input stream
        self.out = [] # output stream
        self.loc = 0 # instruction pointer
        self.done = False # True, once exit instruction is executed

    def input(self, value: int):
        self.inp.append(value)

    def output(self) -> int:
        return self.out.pop(0)

    def run(self) -> bool:
        """Continue execution of the intcode program from the current
        instruction pointer.  Execution will continue until an exit
        instruction is found or we're blocked by input.
        """
        op, pos_mode = parse_instruction(self.mem[self.loc])
        while True:
            # print(
            #     f"[{self.loc:02d}] op {op} mode {pos_mode} "
            #     f"...{','.join([str(v) for v in mem[self.loc:self.loc+4]])} ..."
            # )
            if op == "01":
                a, b, c = self.mem[self.loc + 1], self.mem[self.loc + 2], self.mem[self.loc + 3]
                va = self.mem[a] if pos_mode[0] else a
                vb = self.mem[b] if pos_mode[1] else b
                self.mem[c] = va + vb
                self.loc += 4
            elif op == "02":
                a, b, c = self.mem[self.loc + 1], self.mem[self.loc + 2], self.mem[self.loc + 3]
                va = self.mem[a] if pos_mode[0] else a
                vb = self.mem[b] if pos_mode[1] else b
                self.mem[c] = va * vb
                self.loc += 4
            elif op == "03":
                if not self.inp:
                    break
                a = self.mem[self.loc + 1]
                self.mem[a] = self.inp.pop(0)
                # print(f"self.mem[{a}] <-- input {self.mem[a]}")
                self.loc += 2
            elif op == "04":
                a = self.mem[self.loc + 1]
                self.out.append(self.mem[a])
                # print(f"self.mem[{a}] --> output {self.mem[a]}")
                self.loc += 2
            elif op == "05":
                a, b = self.mem[self.loc + 1], self.mem[self.loc + 2]
                va = self.mem[a] if pos_mode[0] else a
                vb = self.mem[b] if pos_mode[1] else b
                if va:
                    self.loc = vb
                else:
                    self.loc += 3
            elif op == "06":
                a, b = self.mem[self.loc + 1], self.mem[self.loc + 2]
                va = self.mem[a] if pos_mode[0] else a
                vb = self.mem[b] if pos_mode[1] else b
                if not va:
                    self.loc = vb
                else:
                    self.loc += 3
            elif op == "07":
                a, b, c = self.mem[self.loc + 1], self.mem[self.loc + 2], self.mem[self.loc + 3]
                va = self.mem[a] if pos_mode[0] else a
                vb = self.mem[b] if pos_mode[1] else b
                if va < vb:
                    self.mem[c] = 1
                else:
                    self.mem[c] = 0
                self.loc += 4
            elif op == "08":
                a, b, c = self.mem[self.loc + 1], self.mem[self.loc + 2], self.mem[self.loc + 3]
                va = self.mem[a] if pos_mode[0] else a
                vb = self.mem[b] if pos_mode[1] else b
                if va == vb:
                    self.mem[c] = 1
                else:
                    self.mem[c] = 0
                self.loc += 4
            elif op == "99":
                self.done = True
                break
            else:
                raise RuntimeError(f"unrecognized op '{digits}'")
            op, pos_mode = parse_instruction(self.mem[self.loc])

        # print(f"---- {','.join([str(v) for v in self.mem])}")
        return self.done


def parse_instruction(value: int) -> tuple[str, tuple[bool]]:
    """Parse out the opcode and parameter modes for the given integer
    instruction.  A tuple of the opcode (str) and the three parameter
    modes (bools) is returned.
    """
    digits = f"{value:05d}"
    op = digits[3:]
    position_mode = (digits[2] == "0", digits[1] == "0", digits[0] == "0")
    return op, position_mode


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
    mem = init_mem("1002,4,3,4,33")
    proc = IntCode(mem)
    ok = proc.run()
    assert ok
    assert proc.mem[proc.loc] == 99

    # addition of address mode parameters
    mem = init_mem("1,5,6,7,99,8,13,0")
    proc = IntCode(mem)
    ok = proc.run()
    assert ok
    assert proc.mem[7] == 21

    # multiplication of address mode parameters
    mem = init_mem("2,5,6,7,99,8,13,0")
    proc = IntCode(mem)
    ok = proc.run()
    assert ok
    assert proc.mem[7] == 104

    # addition of immediate mode and address mode parameters
    mem = init_mem("101,4,6,7,99,8,13,0")
    proc = IntCode(mem)
    ok = proc.run()
    assert ok
    assert proc.mem[7] == 17

    # multiplication of address mode and immediate mode parameters
    mem = init_mem("1002,5,9,7,99,8,13,0")
    proc = IntCode(mem)
    ok = proc.run()
    assert ok
    assert proc.mem[7] == 72

    # multiplcation of values read from input
    mem = init_mem("3,15,3,16,2,15,16,17,4,17,99", size=20)
    proc = IntCode(mem)
    proc.input(3)
    proc.input(17)
    ok = proc.run()
    assert ok
    assert proc.mem[17] == 51
    assert proc.output() == 51


if __name__ == '__main__':
    test_engine()
    print("all tests passed")
