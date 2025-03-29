import sys
from collections import defaultdict
from math import prod
from typing import Callable

import codyssi.graph as graph
from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
STT -> MFP | 5
AIB -> ZGK | 6
ZGK -> KVX | 20
STT -> AFG | 4
AFG -> ZGK | 16
MFP -> BDD | 13
BDD -> AIB | 5
AXU -> MFP | 4
CLB -> BLV | 20
AIB -> BDD | 13
BLV -> AXU | 17
AFG -> CLB | 2
"""

Output1 = int
Output2 = int
Output3 = int
Edges = dict[str, set[tuple[str, int]]]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(self, input: InputData) -> tuple[set[str], Edges]:
        edges = defaultdict[str, set[tuple[str, int]]](set)
        nodes = set[str]()
        for line in input:
            start, _, end, _, weight = line.split()
            nodes |= {start, end}
            edges[start].add((end, int(weight)))
        return nodes, edges

    def distance(
        self, edges: Edges, end: str, cost: Callable[[str, str], int]
    ) -> int:
        dist, _, _ = graph.dijkstra(
            "STT",
            lambda node: node == end,
            lambda node: (n[0] for n in edges.get(node, [])),
            cost,
        )
        return dist

    def part_1(self, input: InputData) -> Output1:
        nodes, edges = self.parse(input)
        dists = (self.distance(edges, end, lambda _, __: 1) for end in nodes)
        return prod(sorted(dists)[-3:])

    def part_2(self, input: InputData) -> Output2:
        nodes, edges = self.parse(input)
        dists = (
            self.distance(
                edges,
                end,
                lambda node, nxt: next(w for n, w in edges[node] if n == nxt),
            )
            for end in nodes
        )
        return prod(sorted(dists)[-3:])

    def part_3(self, input: InputData) -> Output3:
        nodes, edges = self.parse(input)
        cycle = max(graph.find_cycles(edges, nodes), key=len)
        return sum(
            next(w for n, w in edges[a] if n == b)
            for a, b in zip(cycle, cycle[1:] + [cycle[0]])
        )

    @codyssi_samples(
        (
            ("part_1", TEST, 36),
            ("part_2", TEST, 44720),
            ("part_3", TEST, 18),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(17)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
