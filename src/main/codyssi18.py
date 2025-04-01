import sys
from functools import cache

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
1 ETdhCGi | Quality : 36, Cost : 25, Unique Materials : 7
2 GWgcpkv | Quality : 38, Cost : 17, Unique Materials : 25
3 ODVdJYM | Quality : 1, Cost : 1, Unique Materials : 26
4 wTdbhEr | Quality : 23, Cost : 10, Unique Materials : 18
5 hoOYtHQ | Quality : 25, Cost : 15, Unique Materials : 27
6 jxRouXI | Quality : 31, Cost : 17, Unique Materials : 7
7 dOXpCyA | Quality : 23, Cost : 2, Unique Materials : 28
8 LtCtwHO | Quality : 37, Cost : 26, Unique Materials : 29
9 DLxTAif | Quality : 32, Cost : 24, Unique Materials : 1
10 XCUJAZF | Quality : 22, Cost : 25, Unique Materials : 29
11 cwoqgJA | Quality : 38, Cost : 28, Unique Materials : 7
12 ROPdFSh | Quality : 41, Cost : 29, Unique Materials : 15
13 iYypXES | Quality : 37, Cost : 12, Unique Materials : 15
14 srwmKYA | Quality : 48, Cost : 25, Unique Materials : 14
15 xRbzjOM | Quality : 36, Cost : 20, Unique Materials : 21
"""

Output1 = int
Output2 = int
Output3 = int
Item = tuple[int, int, int]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(self, input: InputData) -> list[Item]:
        items = list[Item]()
        for line in input:
            _, _, _, _, _, q, _, _, c, _, _, _, m = line.split()
            items.append((int(q[:-1]), int(c[:-1]), int(m)))
        return items

    def solve(self, items: list[Item], target: int) -> int:
        @cache
        def get(i: int, cost: int) -> tuple[int, int]:
            if cost == 0:
                return (0, 0)
            qual, mat = 0, 0
            for j in range(i, len(items)):
                if items[j][1] <= cost:
                    res = get(j + 1, cost - items[j][1])
                    nqual = res[0] + items[j][0]
                    nmat = res[1] + items[j][2]
                    if nqual > qual:
                        qual = nqual
                        mat = nmat
                    elif nqual == qual:
                        mat = min(mat, nmat)
            return (qual, mat)

        qual, mat = get(0, target)
        return qual * mat

    def part_1(self, input: InputData) -> Output1:
        return sum(
            m
            for _, _, m in sorted(
                self.parse(input), key=lambda item: item[0] * 100 + item[1]
            )[-5:]
        )

    def part_2(self, input: InputData) -> Output2:
        return self.solve(self.parse(input), target=30)

    def sample_3(self, input: InputData) -> Output3:
        return self.solve(self.parse(input), target=150)

    def part_3(self, input: InputData) -> Output3:
        return self.solve(self.parse(input), target=300)

    @codyssi_samples(
        (
            ("part_1", TEST, 90),
            ("part_2", TEST, 8256),
            ("sample_3", TEST, 59388),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(18)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
