import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
8-9 9-10
7-8 8-10
9-10 5-10
3-10 9-10
4-8 7-9
9-10 2-7
"""

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def ranges(self, line: str) -> tuple[tuple[int, int], tuple[int, int]]:
        n1, n2, n3, n4 = (
            n for split in line.split() for n in map(int, split.split("-"))
        )
        return (n1, n2), (n3, n4)

    def part_1(self, input: InputData) -> Output1:
        return sum(
            hi - lo + 1 for line in input for lo, hi in self.ranges(line)
        )

    def part_2(self, input: InputData) -> Output2:
        return sum(
            len({n for lo, hi in self.ranges(line) for n in range(lo, hi + 1)})
            for line in input
        )

    def part_3(self, input: InputData) -> Output3:
        return max(
            len(
                {
                    n
                    for line in pair
                    for lo, hi in self.ranges(line)
                    for n in range(lo, hi + 1)
                }
            )
            for pair in zip(input, input[1:])
        )

    @codyssi_samples(
        (
            ("part_1", TEST, 43),
            ("part_2", TEST, 35),
            ("part_3", TEST, 9),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(7)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
