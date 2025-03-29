# flake8: noqa E203

import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples
from codyssi.common import to_blocks

TEST = """\
159
527
827
596
296
413
45
796
853
778

4-8
5-8
10-1
6-5
2-1
6-5
8-7
3-6
7-8
2-10
6-4
8-10
1-9
3-6
7-10

10
"""

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(
        self, input: InputData
    ) -> tuple[list[int], list[tuple[int, int]], int]:
        blocks = to_blocks(input)
        freq = list(map(int, blocks[0]))
        swap = []
        for line in blocks[1]:
            x, y = map(lambda n: int(n) - 1, line.split("-"))
            swap.append((x, y))
        test = int(blocks[2][0]) - 1
        return freq, swap, test

    def part_1(self, input: InputData) -> Output1:
        freq, swap, test = self.parse(input)
        for x, y in swap:
            freq[x], freq[y] = freq[y], freq[x]
        return freq[test]

    def part_2(self, input: InputData) -> Output2:
        freq, swap, test = self.parse(input)
        xswap = swap + [swap[0]]
        for i in range(len(swap)):
            x, y, z, _ = *xswap[i], *xswap[i + 1]
            freq[x], freq[y], freq[z] = freq[z], freq[x], freq[y]
        return freq[test]

    def part_3(self, input: InputData) -> Output3:
        freq, swap, test = self.parse(input)
        for x, y in swap:
            x, y = sorted((x, y))
            size = min(y - x, len(freq) - y)
            freq = (
                freq[:x]
                + freq[y : y + size]
                + freq[x + size : y]
                + freq[x : x + size]
                + freq[y + size :]
            )
        return freq[test]

    @codyssi_samples(
        (
            ("part_1", TEST, 45),
            ("part_2", TEST, 796),
            ("part_3", TEST, 827),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(11)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
