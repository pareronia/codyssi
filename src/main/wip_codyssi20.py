import itertools
import sys
from math import prod

from prettyprinter import pretty_call
from prettyprinter import register_pretty

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import clog
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
TEST3 = """\
FACE - VALUE 99
FACE - VALUE 10
ROW 1 - VALUE 20
COL 80 - VALUE 30
FACE - VALUE 40
ROW 2 - VALUE 50
COL 78 - VALUE 60
FACE - VALUE 70
ROW 3 - VALUE 80
COL 77 - VALUE 90
FACE - VALUE 11
ROW 4 - VALUE 21
COL 76 - VALUE 31
FACE - VALUE 41
ROW 5 - VALUE 51
COL 75 - VALUE 61
FACE - VALUE 71
ROW 6 - VALUE 81
COL 74 - VALUE 91
FACE - VALUE 12
ROW 7 - VALUE 22
COL 73 - VALUE 32
FACE - VALUE 42
ROW 8 - VALUE 52
COL 72 - VALUE 62
FACE - VALUE 72
ROW 9 - VALUE 82
COL 71 - VALUE 92

ULDDRUURDRULRDLLURLDRLURLLL
"""

Output1 = int
Output2 = int
Output3 = int
U, D, L, R = "U", "D", "L", "R"
TWISTS = {
    1: {
        0: {U: (4, 0), D: (2, 0), R: (6, 3), L: (5, 1)},
        1: {U: (5, 2), D: (6, 0), R: (4, 1), L: (2, 1)},
        2: {U: (2, 2), D: (4, 2), R: (5, 3), L: (6, 1)},
        3: {U: (6, 2), D: (5, 0), R: (2, 3), L: (4, 3)},
    },
    2: {
        0: {U: (1, 0), D: (3, 0), R: (6, 0), L: (5, 0)},
        1: {U: (5, 1), D: (6, 1), R: (1, 1), L: (3, 1)},
        2: {U: (3, 2), D: (1, 2), R: (5, 2), L: (6, 2)},
        3: {U: (6, 3), D: (5, 3), R: (3, 3), L: (1, 3)},
    },
    3: {
        0: {U: (2, 0), D: (4, 0), R: (6, 1), L: (5, 3)},
        1: {U: (5, 0), D: (6, 2), R: (2, 1), L: (4, 1)},
        2: {U: (4, 2), D: (2, 2), R: (5, 1), L: (6, 3)},
        3: {U: (6, 0), D: (5, 2), R: (4, 3), L: (2, 3)},
    },
    4: {
        0: {U: (3, 0), D: (1, 0), R: (6, 2), L: (5, 2)},
        1: {U: (5, 3), D: (6, 3), R: (3, 1), L: (1, 1)},
        2: {U: (1, 2), D: (3, 2), R: (5, 0), L: (6, 0)},
        3: {U: (6, 1), D: (5, 1), R: (1, 3), L: (3, 3)},
    },
    5: {
        0: {U: (1, 3), D: (3, 1), R: (2, 0), L: (4, 2)},
        1: {U: (4, 3), D: (2, 1), R: (1, 0), L: (3, 2)},
        2: {U: (3, 3), D: (1, 1), R: (4, 0), L: (2, 2)},
        3: {U: (2, 3), D: (4, 1), R: (3, 0), L: (1, 2)},
    },
    6: {
        0: {U: (1, 1), D: (3, 3), R: (4, 2), L: (2, 0)},
        1: {U: (2, 1), D: (4, 3), R: (1, 2), L: (3, 0)},
        2: {U: (3, 1), D: (1, 3), R: (2, 2), L: (4, 0)},
        3: {U: (4, 1), D: (2, 3), R: (3, 2), L: (1, 0)},
    },
}


class Cube:
    def __init__(self, size: int) -> None:
        self.size = size
        self.grids = {
            i: [[1 for _ in range(size)] for _ in range(size)]
            for i in range(1, 7)
        }
        self.current = (1, 0)
        self.absorptions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    def add(self, row: int, col: int, val: int) -> None:
        front, _ = self.current
        self.grids[front][row][col] += val
        if self.grids[front][row][col] > 100:
            self.grids[front][row][col] -= 100

    def add_face(self, val: int) -> None:
        self.absorptions[self.current[0]] += val * self.size * self.size
        for r in range(self.size):
            for c in range(self.size):
                self.add(r, c, val)

    def add_row(self, row: int, val: int) -> None:
        front, rotations = self.current
        self.absorptions[front] += val * self.size
        match rotations:
            case 0:
                self.do_add_row(row, val)
            case 1:
                self.do_add_col(row, val)
            case 2:
                self.do_add_row(self.size - 1 - row, val)
            case 3:
                self.do_add_col(self.size - 1 - row, val)

    def do_add_row(self, row: int, val: int) -> None:
        for c in range(self.size):
            self.add(row, c, val)

    def add_col(self, col: int, val: int) -> None:
        front, rotations = self.current
        self.absorptions[front] += val * self.size
        match rotations:
            case 0:
                self.do_add_col(col, val)
            case 1:
                self.do_add_row(self.size - 1 - col, val)
            case 2:
                self.do_add_col(self.size - 1 - col, val)
            case 3:
                self.do_add_row(col, val)

    def do_add_col(self, col: int, val: int) -> None:
        for r in range(self.size):
            self.add(r, col, val)

    def dominant_sum(self, idx: int) -> int:
        return max(
            sum(self.grids[idx][r][c] for r, c in rc)
            for rc in itertools.chain(
                (((r, c) for c in range(self.size)) for r in range(self.size)),
                (((r, c) for r in range(self.size)) for c in range(self.size)),
            )
        )

    def log_line(
        self, line: str, rotation: str
    ) -> tuple[str, tuple[int, int], str, str]:
        return (
            line,
            self.current,
            rotation,
            ",".join(
                str(_)
                for _ in (
                    sorted(
                        (self.dominant_sum(idx) for idx in range(1, 7)),
                        reverse=True,
                    )
                )
            ),
        )


@register_pretty(Cube)
def pretty_cube(value, ctx):  # type:ignore
    return pretty_call(ctx, Cube, front=value.front, grids=value.grids)


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input: InputData, cube: Cube) -> None:
        blocks = to_blocks(input)
        for line, rotation in itertools.zip_longest(blocks[0], blocks[1][0]):
            left, right = line.split(" - ")
            target = left.split()[0]
            val = int(right.split()[-1])
            match target:
                case "FACE":
                    cube.add_face(val)
                case "COL":
                    col = int(left.split()[1]) - 1
                    cube.add_col(col, val)
                case "ROW":
                    row = int(left.split()[1]) - 1
                    cube.add_row(row, val)
            clog(lambda: cube.log_line(line, rotation))
            if rotation is not None:
                front, rotations = cube.current
                cube.current = TWISTS[front][rotations][rotation]

    def solve_1(self, input: InputData, size: int) -> Output1:
        cube = Cube(size)
        self.solve(input, cube)
        return prod(sorted(cube.absorptions.values())[-2:])

    def part_1(self, input: InputData) -> Output1:
        return self.solve_1(input, 80)

    def solve_2(self, input: InputData, size: int) -> Output2:
        cube = Cube(size)
        self.solve(input, cube)
        return prod(cube.dominant_sum(idx) for idx in range(1, 7))

    def part_2(self, input: InputData) -> Output2:
        return self.solve_2(input, 80)

    def part_3(self, input: InputData) -> Output3:
        return 0

    def samples(self) -> None:
        assert (
            self.solve_2(tuple(TEST3.splitlines()), 80)
            == 41477439119464857600000
        )
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
