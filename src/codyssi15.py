import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
32IED4E6L4 22
1111300022221031003013 4
1C1117A3BA88 13
1100010000010010010001111000000010001100101 2
7AJ5G2AB4F 22
k6IHxTD 61
"""

Output1 = int
Output2 = str
Output3 = int
BASE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^"


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        def to_int(val: str, base: int) -> int:
            i = 0
            for j, ch in enumerate(val):
                i += BASE.find(ch) * base ** (len(val) - 1 - j)
            return i

        ans = 0
        for line in input:
            val, b = line.split()
            ans = max(to_int(val, int(b)), ans)
        return ans

    def part_2(self, input: InputData) -> Output2:
        def to_int(val: str, base: int) -> int:
            i = 0
            for j, ch in enumerate(val):
                i += BASE.find(ch) * base ** (len(val) - 1 - j)
            return i

        tot = 0
        for line in input:
            val, b = line.split()
            tot += to_int(val, int(b))
        ans = ""
        while tot > 0:
            mod = tot % 68
            ans += BASE[mod]
            tot //= 68
        return ans[::-1]

    def part_3(self, input: InputData) -> Output3:
        def to_int(val: str, base: int) -> int:
            i = 0
            for j, ch in enumerate(val):
                i += BASE.find(ch) * base ** (len(val) - 1 - j)
            return i

        tot = 0
        for line in input:
            val, b = line.split()
            tot += to_int(val, int(b))
        for n in range(10_000, -1, -1):
            top = n**4 - 1
            if top <= tot:
                break
        return n + 1

    @codyssi_samples(
        (
            ("part_1", TEST, 9047685997827),
            ("part_2", TEST, "4iWAbo%6"),
            ("part_3", TEST, 2366),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(15)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
