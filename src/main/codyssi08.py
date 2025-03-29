import itertools
import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
NNBUSSSSSDSSZZZZMMMMMMMM
PWAAASYBRRREEEEEEE
FBBOFFFKDDDDDDDDD
VJAANCPKKLZSSSSSSSSS
NNNNNNBBVVVVVVVVV
"""

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def memory_units(self, line: str) -> int:
        return sum(
            int(ch) if ch.isnumeric() else ord(ch) - ord("A") + 1
            for ch in line
        )

    def part_1(self, input: InputData) -> Output1:
        return sum(self.memory_units(line) for line in input)

    def part_2(self, input: InputData) -> Output2:
        return sum(
            self.memory_units(
                f"{line[:keep]}{len(line) - keep * 2}{line[-keep:]}"
            )
            for line, keep in map(lambda x: (x, len(x) // 10), input)
        )

    def part_3(self, input: InputData) -> Output3:
        return sum(
            self.memory_units(
                "".join(
                    map(
                        lambda x: f"{len(list(x[1]))}{x[0]}",
                        itertools.groupby(line),
                    )
                )
            )
            for line in input
        )

    @codyssi_samples(
        (
            ("part_1", TEST, 1247),
            ("part_2", TEST, 219),
            ("part_3", TEST, 539),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(8)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
