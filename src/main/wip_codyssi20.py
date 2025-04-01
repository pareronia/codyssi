import itertools
import sys
from math import prod

from prettyprinter import pretty_call
from prettyprinter import register_pretty

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import log
from codyssi.common import to_blocks

TEST1 = """\
FACE - VALUE 38
ROW 2 - VALUE 71
ROW 1 - VALUE 57
ROW 3 - VALUE 68
COL 1 - VALUE 52

LURD
"""
TEST2 = """\
FACE - VALUE 38
COL 32 - VALUE 39
COL 72 - VALUE 12
COL 59 - VALUE 56
COL 77 - VALUE 31
FACE - VALUE 43
COL 56 - VALUE 47
ROW 73 - VALUE 83
COL 15 - VALUE 87
COL 76 - VALUE 57

ULDLRLLRU
"""

Output1 = int
Output2 = int
Output3 = int


class Cube:
    def __init__(self, size: int) -> None:
        self.size = size
        self.front = 1
        self.top = 4
        self.right = 6
        self.bottom = 2
        self.left = 5
        self.back = 3
        self.grids = {
            i: [[1 for _ in range(size)] for _ in range(size)]
            for i in range(1, 7)
        }
        self.rotations = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.rotate_grid(6)
        for _ in range(3):
            self.rotate_grid(5)

    def rotate_x(self) -> None:
        self.rotate_grid(self.left)
        for _ in range(3):
            self.rotate_grid(self.right)
        self.front, self.top, self.right, self.bottom, self.left, self.back = (
            self.bottom,
            self.front,
            self.right,
            self.back,
            self.left,
            self.top,
        )

    def rotate_y(self) -> None:
        self.rotate_grid(self.bottom)
        for _ in range(3):
            self.rotate_grid(self.top)
        self.front, self.top, self.right, self.bottom, self.left, self.back = (
            self.right,
            self.top,
            self.back,
            self.bottom,
            self.front,
            self.left,
        )

    def rotate_grid(self, idx: int) -> None:
        self.rotations[idx] = (self.rotations[idx] + 1) % 4

    def add_face(self, val: int) -> None:
        for r in range(self.size):
            for c in range(self.size):
                self.grids[self.front][r][c] = (
                    self.grids[self.front][r][c] + val
                ) % 100

    def add_row(self, row: int, val: int) -> None:
        match self.rotations[self.front]:
            case 0:
                self.do_add_row(row, val)
            case 1:
                self.do_add_col(self.size - 1 - row, val)
            case 2:
                self.do_add_row(self.size - 1 - row, val)
            case 3:
                self.do_add_col(row, val)

    def do_add_row(self, row: int, val: int) -> None:
        for c in range(self.size):
            self.grids[self.front][row][c] = (
                self.grids[self.front][row][c] + val
            ) % 100

    def add_col(self, col: int, val: int) -> None:
        match self.rotations[self.front]:
            case 0:
                self.do_add_col(col, val)
            case 1:
                self.do_add_row(col, val)
            case 2:
                self.do_add_row(self.size - 1 - col, val)
            case 3:
                self.do_add_row(self.size - 1 - col, val)

    def do_add_col(self, col: int, val: int) -> None:
        for r in range(self.size):
            self.grids[self.front][r][col] = (
                self.grids[self.front][r][col] + val
            ) % 100


@register_pretty(Cube)
def pretty_cube(value, ctx):  # type:ignore
    return pretty_call(ctx, Cube, front=value.front, grids=value.grids)


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve_1(self, input: InputData, size: int) -> Output1:
        blocks = to_blocks(input)
        cube = Cube(size)
        absorptions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for line, rotation in itertools.zip_longest(blocks[0], blocks[1][0]):
            left, right = line.split(" - ")
            target = left.split()[0]
            val = int(right.split()[-1])
            match target:
                case "FACE":
                    absorptions[cube.front] += val * size * size
                    cube.add_face(val)
                case "COL":
                    absorptions[cube.front] += val * size
                    col = int(left.split()[1]) - 1
                    cube.add_col(col, val)
                case "ROW":
                    absorptions[cube.front] += val * size
                    row = int(left.split()[1]) - 1
                    cube.add_row(row, val)
            match rotation:
                case "L":
                    for _ in range(3):
                        cube.rotate_y()
                case "R":
                    cube.rotate_y()
                case "D":
                    for _ in range(3):
                        cube.rotate_x()
                case "U":
                    cube.rotate_x()
        return prod(sorted(absorptions.values())[-2:])

    def part_1(self, input: InputData) -> Output1:
        return self.solve_1(input, 80)

    def solve_2(self, input: InputData, size: int) -> Output2:
        blocks = to_blocks(input)
        cube = Cube(size)
        # log(cube)
        absorptions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for line, rotation in itertools.zip_longest(blocks[0], blocks[1][0]):
            left, right = line.split(" - ")
            target = left.split()[0]
            val = int(right.split()[-1])
            match target:
                case "FACE":
                    absorptions[cube.front] += val * size * size
                    cube.add_face(val)
                case "COL":
                    absorptions[cube.front] += val * size
                    col = int(left.split()[1]) - 1
                    cube.add_col(col, val)
                case "ROW":
                    absorptions[cube.front] += val * size
                    row = int(left.split()[1]) - 1
                    cube.add_row(row, val)
            match rotation:
                case "L":
                    for _ in range(3):
                        cube.rotate_y()
                case "R":
                    cube.rotate_y()
                case "D":
                    cube.rotate_x()
                case "U":
                    for _ in range(3):
                        cube.rotate_x()
        # log(cube)
        ans = prod(
            max(
                sum(cube.grids[idx][r][c] for r, c in rc)
                for rc in itertools.chain(
                    (
                        ((r, c) for c in range(cube.size))
                        for r in range(cube.size)
                    ),
                    (
                        ((r, c) for r in range(cube.size))
                        for c in range(cube.size)
                    ),
                )
            )
            for idx in range(1, 7)
        )
        log(ans)
        return ans

    def part_2(self, input: InputData) -> Output2:
        return self.solve_2(input, 80)

    def part_3(self, input: InputData) -> Output3:
        log("hey")
        return 0

    def samples(self) -> None:
        assert self.solve_1(tuple(TEST1.splitlines()), 3) == 201474
        assert self.solve_1(tuple(TEST2.splitlines()), 80) == 6902016000
        assert self.solve_2(tuple(TEST1.splitlines()), 3) == 118727856
        assert (
            self.solve_2(tuple(TEST2.splitlines()), 80)
            == 369594451623936000000
        )
        assert self.part_3(tuple(TEST1.splitlines())) == 0


solution = Solution(20)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
