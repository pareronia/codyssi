import itertools
import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
8
1
5
5
7
6
5
4
3
1
-++-++-++
"""

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(
        self, input: InputData, count: int, reverse: bool, batch: int
    ) -> int:
        magnitudes = list(
            map(
                lambda x: int("".join(x)),
                itertools.batched(input[:count], batch),
            )
        )
        signs = [1] + list(
            map(
                lambda x: 1 if x == "+" else -1,
                reversed(input[count]) if reverse else input[count],
            )
        )
        return sum(sign * mag for sign, mag in zip(signs, magnitudes))

    def sample_1(self, input: InputData) -> Output1:
        return self.solve(input, count=10, reverse=False, batch=1)

    def sample_2(self, input: InputData) -> Output2:
        return self.solve(input, count=10, reverse=True, batch=1)

    def sample_3(self, input: InputData) -> Output3:
        return self.solve(input, count=10, reverse=True, batch=2)

    def part_1(self, input: InputData) -> Output1:
        return self.solve(input, count=600, reverse=False, batch=1)

    def part_2(self, input: InputData) -> Output2:
        return self.solve(input, count=600, reverse=True, batch=1)

    def part_3(self, input: InputData) -> Output3:
        return self.solve(input, count=600, reverse=True, batch=2)

    @codyssi_samples(
        (
            ("sample_1", TEST, 21),
            ("sample_2", TEST, 23),
            ("sample_3", TEST, 189),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(5)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
