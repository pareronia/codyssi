import itertools
import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
TRUE
FALSE
TRUE
FALSE
FALSE
FALSE
TRUE
TRUE
"""

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(self, input: InputData) -> list[bool]:
        return list(map(lambda x: x == "TRUE", input))

    def reduce(self, sensors: list[bool]) -> list[bool]:
        return [
            (vals[0] or vals[1]) if i % 2 else (vals[0] and vals[1])
            for i, vals in enumerate(itertools.batched(sensors, 2))
        ]

    def part_1(self, input: InputData) -> Output1:
        return sum(
            id for id, val in enumerate(self.parse(input), start=1) if val
        )

    def part_2(self, input: InputData) -> Output2:
        return sum(self.reduce(self.parse(input)))

    def part_3(self, input: InputData) -> Output3:
        sensors = self.parse(input)
        ans = sum(sensors)
        while len(sensors) > 1:
            sensors = self.reduce(sensors)
            ans += sum(sensors)
        return ans

    @codyssi_samples(
        (
            ("part_1", TEST, 19),
            ("part_2", TEST, 2),
            ("part_3", TEST, 7),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
