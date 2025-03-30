import sys

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
        dp = [[(0, 0)] * (target + 1) for _ in range(len(items) + 1)]
        for i, item in enumerate(items, start=1):
            qual, cost, mat = item
            for j in range(target + 1):
                if cost <= j:
                    prev = dp[i - 1][j - cost]
                    dp[i][j] = max(
                        dp[i - 1][j],
                        (prev[0] + qual, prev[1] - mat),
                    )
                else:
                    dp[i][j] = dp[i - 1][j]
        best = []
        j = target
        for i in range(len(items), 0, -1):
            if dp[i][j] != dp[i - 1][j]:
                best.append(items[i - 1])
                j -= items[i - 1][1]
        return sum(q for q, _, _ in best) * sum(m for _, _, m in best)

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
