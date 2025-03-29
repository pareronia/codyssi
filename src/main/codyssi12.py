import sys
from enum import Enum
from enum import auto
from enum import unique

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
tv8cmj0i2951190z5w44fe205k542l5818ds05ib425h9lj260ud38-l6a06
a586m0eeuqqvt5-k-8434hb27ytha3i75-lw23-0cj856l7zn8234a05eron
"""

Output1 = int
Output2 = int
Output3 = int


@unique
class Reduction(Enum):
    MODE_1 = auto()
    MODE_2 = auto()

    def test(self, ch: str) -> bool:
        match self:
            case Reduction.MODE_1:
                return ch.isalpha() or ch == "-"
            case Reduction.MODE_2:
                return ch.isalpha()

    def reduce(self, line: str) -> list[str]:
        ans = [ch for ch in line]
        while True:
            remove = set[int]()
            for n in [i for i, ch in enumerate(ans) if ch.isnumeric()]:
                if (
                    n > 0
                    and len(remove & {n, n - 1}) == 0
                    and self.test(ans[n - 1])
                ):
                    remove |= {n, n - 1}
                if (
                    n < len(ans) - 1
                    and len(remove & {n, n + 1}) == 0
                    and self.test(ans[n + 1])
                ):
                    remove |= {n, n + 1}
            if len(remove) == 0:
                break
            ans = [ch for i, ch in enumerate(ans) if i not in remove]
        return ans


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        return sum(1 for line in input for ch in line if ch.isalpha())

    def part_2(self, input: InputData) -> Output2:
        return sum(len(Reduction.MODE_1.reduce(line)) for line in input)

    def part_3(self, input: InputData) -> Output3:
        return sum(len(Reduction.MODE_2.reduce(line)) for line in input)

    @codyssi_samples(
        (
            ("part_1", TEST, 52),
            ("part_2", TEST, 18),
            ("part_3", TEST, 26),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(12)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
