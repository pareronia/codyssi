import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
100011101111110010101101110011 2
83546306 10
1106744474 8
170209FD 16
2557172641 8
2B290C15 16
279222446 10
6541027340 8
"""

Output1 = int
Output2 = int
Output3 = str
BASE_65 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#"


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        return sum(int(line.split()[1]) for line in input)

    def get_sum(self, input: InputData) -> int:
        def get_val(line: str) -> int:
            reading, base = line.split()
            return int(reading, int(base))

        return sum(get_val(line) for line in input)

    def part_2(self, input: InputData) -> Output2:
        return self.get_sum(input)

    def part_3(self, input: InputData) -> Output3:
        ans = ""
        tot = self.get_sum(input)
        while tot > 0:
            ans += BASE_65[tot % 65]
            tot //= 65
        return ans[::-1]

    @codyssi_samples(
        (
            ("part_1", TEST, 78),
            ("part_2", TEST, 3487996082),
            ("part_3", TEST, "30PzDC"),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(3)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
