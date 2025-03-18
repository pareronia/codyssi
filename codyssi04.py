import sys
from collections import defaultdict

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples
from codyssi.graph import dijkstra

TEST = """\
ADB <-> XYZ
STT <-> NYC
PLD <-> XYZ
ADB <-> NYC
JLI <-> NYC
PTO <-> ADB
"""

Output1 = int
Output2 = int
Output3 = int
Edges = dict[str, set[str]]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def get_edges(self, input: InputData) -> Edges:
        edges = defaultdict[str, set[str]](set)
        for line in input:
            loc1, loc2 = line.split(" <-> ")
            edges[loc1].add(loc2)
            edges[loc2].add(loc1)
        return edges

    def get_distances(self, edges: Edges) -> dict[str, int]:
        ans = dict[str, int]()
        for loc in edges:
            cost, _, _ = dijkstra(
                "STT",
                lambda curr: curr == loc,
                lambda curr: (n for n in edges[curr]),
                lambda curr, _: 1,
            )
            ans[loc] = cost
        return ans

    def part_1(self, input: InputData) -> Output1:
        return len(self.get_edges(input))

    def part_2(self, input: InputData) -> Output2:
        return sum(
            1
            for d in self.get_distances(self.get_edges(input)).values()
            if d <= 3
        )

    def part_3(self, input: InputData) -> Output3:
        return sum(self.get_distances(self.get_edges(input)).values())

    @codyssi_samples(
        (
            ("part_1", TEST, 7),
            ("part_2", TEST, 6),
            ("part_3", TEST, 15),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(4)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
