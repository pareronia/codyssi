import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase

TEST = """\
912372
283723
294281
592382
721395
91238
"""

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        return sum(map(int, input))

    def solve_2(self, input: InputData, discount: int) -> int:
        prices = list(sorted(map(int, input), reverse=True))
        return sum(prices[discount:])

    def part_2(self, input: InputData) -> Output2:
        return self.solve_2(input, 20)

    def part_3(self, input: InputData) -> Output3:
        return sum(
            (-1 if i % 2 else 1) * price
            for i, price in enumerate(map(int, input))
        )

    def samples(self) -> None:
        assert self.part_1(tuple(TEST.splitlines())) == 2895391
        assert self.solve_2(tuple(TEST.splitlines()), 2) == 1261624
        assert self.part_3(tuple(TEST.splitlines())) == 960705


solution = Solution(1)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
