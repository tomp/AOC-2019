#!/usr/bin/env python3
"""
Intcode processor simulator
"""
from typing import Optional


def run_intcode(
    input_mem: list[int],
    inp: Optional[list[int]] = None,
    out: Optional[list[int]] = None,
) -> list[int]:
    """Execute the intcode program in input_mem (the initial memory image)
    with the given (optional) input and output streams.  The input and
    output streams are modified in-place.  If input or output is required
    and the input o output stream wasn't provided, and exception is raised.
    The final memory image is returned.
    """
    mem = list(input_mem)
    loc = 0  # current position
    op, pos_mode = parse_instruction(mem[loc])
    while op != "99":
        # print(
        #     f"[{loc:02d}] op {op} mode {pos_mode} "
        #     f"...{','.join([str(v) for v in mem[loc:loc+4]])} ..."
        # )
        if op == "01":
            a, b, c = mem[loc + 1], mem[loc + 2], mem[loc + 3]
            va = mem[a] if pos_mode[0] else a
            vb = mem[b] if pos_mode[1] else b
            mem[c] = va + vb
            loc += 4
        elif op == "02":
            a, b, c = mem[loc + 1], mem[loc + 2], mem[loc + 3]
            va = mem[a] if pos_mode[0] else a
            vb = mem[b] if pos_mode[1] else b
            mem[c] = va * vb
            loc += 4
        elif op == "03":
            a = mem[loc + 1]
            mem[a] = inp.pop(0)
            print(f"mem[{a}] <-- input {mem[a]}")
            loc += 2
        elif op == "04":
            a = mem[loc + 1]
            out.append(mem[a])
            print(f"mem[{a}] --> output {mem[a]}")
            loc += 2
        elif op == "05":
            a, b = mem[loc + 1], mem[loc + 2]
            va = mem[a] if pos_mode[0] else a
            vb = mem[b] if pos_mode[1] else b
            if va:
                loc = vb
            else:
                loc += 3
        elif op == "06":
            a, b = mem[loc + 1], mem[loc + 2]
            va = mem[a] if pos_mode[0] else a
            vb = mem[b] if pos_mode[1] else b
            if not va:
                loc = vb
            else:
                loc += 3
        elif op == "07":
            a, b, c = mem[loc + 1], mem[loc + 2], mem[loc + 3]
            va = mem[a] if pos_mode[0] else a
            vb = mem[b] if pos_mode[1] else b
            if va < vb:
                mem[c] = 1
            else:
                mem[c] = 0
            loc += 4
        elif op == "08":
            a, b, c = mem[loc + 1], mem[loc + 2], mem[loc + 3]
            va = mem[a] if pos_mode[0] else a
            vb = mem[b] if pos_mode[1] else b
            if va == vb:
                mem[c] = 1
            else:
                mem[c] = 0
            loc += 4
        else:
            raise RuntimeError(f"unrecognized op '{digits}'")
        op, pos_mode = parse_instruction(mem[loc])

    # print(f"---- {','.join([str(v) for v in mem])}")
    return mem


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
    final = run_intcode(mem)
    assert final[4] == 99

    # addition of address mode parameters
    mem = init_mem("1,5,6,7,99,8,13,0")
    final = run_intcode(mem)
    assert final[7] == 21

    # multiplication of address mode parameters
    mem = init_mem("2,5,6,7,99,8,13,0")
    final = run_intcode(mem)
    assert final[7] == 104

    # addition of immediate mode and address mode parameters
    mem = init_mem("101,4,6,7,99,8,13,0")
    final = run_intcode(mem)
    assert final[7] == 17

    # multiplication of address mode and immediate mode parameters
    mem = init_mem("1002,5,9,7,99,8,13,0")
    final = run_intcode(mem)
    assert final[7] == 72

    # multiplcation of values read from input
    mem = init_mem("3,15,3,16,2,15,16,17,4,17,99", size=20)
    inputs = [3, 17]
    outputs = []
    final = run_intcode(mem, inp=inputs, out=outputs)
    assert final[17] == 51
    assert outputs[0] == 51


if __name__ == '__main__':
    test_engine()
    print("all tests passed")
