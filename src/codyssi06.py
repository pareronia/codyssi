import sys
from typing import Callable

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples
from codyssi.common import to_blocks

TEST = """\
Function A: ADD 495
Function B: MULTIPLY 55
Function C: RAISE TO THE POWER OF 3

5219
8933
3271
7128
9596
9407
7005
1607
4084
4525
5496
"""

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(
        self, input: InputData
    ) -> tuple[list[int], Callable[[int], int]]:
        blocks = to_blocks(input)
        add = int(blocks[0][0].split()[-1])
        mul = int(blocks[0][1].split()[-1])
        exp = int(blocks[0][2].split()[-1])
        prices = list(map(int, blocks[1]))
        return prices, lambda x: int(x**exp * mul + add)

    def part_1(self, input: InputData) -> Output1:
        prices, calc = self.parse(input)
        return calc(sorted(prices)[len(prices) // 2])

    def part_2(self, input: InputData) -> Output2:
        prices, calc = self.parse(input)
        return calc(sum(p for p in prices if p % 2 == 0))

    def part_3(self, input: InputData) -> Output3:
        prices, calc = self.parse(input)
        return next(
            p
            for p in sorted(prices, reverse=True)
            if calc(p) <= 15000000000000
        )

    @codyssi_samples(
        (
            ("part_1", TEST, 9130674516975),
            ("part_2", TEST, 1000986169836015),
            ("part_3", TEST, 5496),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(6)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
