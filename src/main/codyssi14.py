import itertools
import sys
from typing import Iterator
from typing import NamedTuple
from typing import Self

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples
from codyssi.graph import dijkstra

TEST = """\
3 3 1 7 8 4 1 3 1 7 7 6 7 8 7 8 2 7 7 1
9 9 7 6 3 6 9 4 9 2 6 4 5 7 3 9 3 7 5 6
8 9 7 6 7 7 3 2 2 7 8 9 7 1 5 3 1 2 4 4
9 2 8 2 3 5 9 2 6 5 7 8 1 6 7 3 6 7 9 6
4 1 7 5 2 2 7 6 8 7 2 3 9 2 2 1 6 2 7 5
2 9 1 2 9 9 1 2 2 9 3 7 4 5 3 3 7 1 9 4
9 9 5 2 6 6 2 3 1 8 3 3 3 6 7 9 8 3 1 5
8 4 8 7 2 1 7 9 8 7 3 7 9 1 8 5 2 5 2 8
6 8 9 6 6 4 2 2 7 7 7 8 1 2 6 2 6 1 6 7
3 8 8 6 9 9 2 7 8 5 4 1 8 8 5 8 3 5 6 6
2 8 7 2 6 8 4 7 1 7 6 8 9 4 3 1 2 8 9 8
6 2 9 7 7 2 8 7 9 5 6 6 8 2 8 4 4 8 2 2
3 1 2 8 8 4 6 8 9 1 4 3 9 1 4 2 2 1 5 4
5 2 6 7 2 7 3 9 2 1 7 6 1 2 4 2 1 1 5 9
3 6 8 9 4 4 7 7 3 3 4 8 6 1 2 9 7 2 9 6
9 4 5 5 7 4 1 7 7 1 3 2 3 8 1 7 6 3 1 9
5 3 8 3 1 1 5 3 1 5 9 2 3 6 6 4 4 8 5 3
6 3 8 2 9 7 3 6 4 3 2 8 6 9 8 1 2 7 1 5
4 1 2 4 8 7 7 1 8 7 4 4 5 7 2 3 3 8 3 3
1 5 7 3 3 5 1 5 4 1 1 1 9 2 1 4 6 5 6 3
"""

Output1 = int
Output2 = int
Output3 = int


class Grid(NamedTuple):
    grid: list[list[int]]
    grid_size: int

    @classmethod
    def from_input(cls, input: InputData) -> Self:
        grid = [list(map(int, line.split())) for line in input]
        return cls(grid, len(grid))

    @property
    def size(self) -> int:
        return self.grid_size

    def danger_level(self, path: Iterator[tuple[int, int]]) -> int:
        return sum(self.grid[r][c] for r, c in path)

    def safest_path(self, end: tuple[int, int]) -> int:
        _, _, path = dijkstra(
            (0, 0),
            lambda cell: cell == end,
            lambda cell: (
                n
                for n in {(cell[0], cell[1] + 1), (cell[0] + 1, cell[1])}
                if n[0] < self.size and n[1] < self.size
            ),
            lambda curr, nxt: self.grid[nxt[0]][nxt[1]],
        )
        return self.danger_level(((r, c) for r, c in path))


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        grid = Grid.from_input(input)
        return min(
            itertools.chain(
                (
                    grid.danger_level(((r, c) for c in range(grid.size)))
                    for r in range(grid.size)
                ),
                (
                    grid.danger_level(((r, c) for r in range(grid.size)))
                    for c in range(grid.size)
                ),
            )
        )

    def part_2(self, input: InputData) -> Output2:
        grid = Grid.from_input(input)
        return grid.safest_path(end=(14, 14))

    def part_3(self, input: InputData) -> Output3:
        grid = Grid.from_input(input)
        return grid.safest_path(end=(grid.size - 1, grid.size - 1))

    @codyssi_samples(
        (
            ("part_1", TEST, 73),
            ("part_2", TEST, 94),
            ("part_3", TEST, 120),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(14)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
