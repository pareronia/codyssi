from __future__ import annotations

import sys
from typing import Iterable
from typing import NamedTuple

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
(-16, -191)
(92, 186)
(157, -75)
(39, -132)
(-42, 139)
(-74, -150)
(200, 197)
(-106, 105)
"""


class Position(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_input(_cls, line: str) -> Position:
        x, y = map(int, line.split(", "))
        return Position(x, y)

    def md(self, other: Position) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class Distance(NamedTuple):
    position: Position
    value: int

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Distance):
            raise NotImplementedError()
        if self.value == other.value:
            return (
                self.position.x == other.position.x
                and self.position.y < other.position.y
                or self.position.x < other.position.x
            )
        return self.value < other.value


Output1 = int
Output2 = int
Output3 = int
START = Position(0, 0)


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(self, input: InputData) -> set[Position]:
        return {
            Position.from_input(line)
            for line in map(lambda x: x[1:][:-1], input)
        }

    def distances(
        self, positions: Iterable[Position], to: Position
    ) -> list[Distance]:
        return sorted(Distance(p, p.md(to)) for p in positions if p != to)

    def part_1(self, input: InputData) -> Output1:
        distances = self.distances(self.parse(input), START)
        return abs(distances[0].value - distances[-1].value)

    def part_2(self, input: InputData) -> Output2:
        positions = self.parse(input)
        closest1 = self.distances(positions, START)[0]
        closest2 = self.distances(positions, closest1.position)[0]
        return closest1.position.md(closest2.position)

    def part_3(self, input: InputData) -> Output3:
        positions = self.parse(input)
        path = [Distance(START, 0)]
        while len(path) <= len(positions):
            path.append(
                self.distances(
                    positions - {d.position for d in path}, path[-1].position
                )[0]
            )
        return sum(d.value for d in path)

    @codyssi_samples(
        (
            ("part_1", TEST, 226),
            ("part_2", TEST, 114),
            ("part_3", TEST, 1384),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(9)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
