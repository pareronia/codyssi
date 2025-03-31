import sys
from collections import defaultdict

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples
from codyssi.common import to_blocks

TEST = """\
ozNxANO | 576690
pYNonIG | 323352
MUantNm | 422646
lOSlxki | 548306
SDJtdpa | 493637
ocWkKQi | 747973
qfSKloT | 967749
KGRZQKg | 661714
JSXfNAJ | 499862
LnDiFPd | 55528
FyNcJHX | 9047
UfWSgzb | 200543
PtRtdSE | 314969
gwHsSzH | 960026
JoyLmZv | 833936

MUantNm | 422646
FyNcJHX | 9047
"""

Output1 = int
Output2 = str
Output3 = str


class Node:
    def __init__(self, val: tuple[int, str]):
        self.val: tuple[int, str] = val
        self.left: Node | None = None
        self.right: Node | None = None


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(
        self, input: list[str]
    ) -> tuple[list[tuple[int, str]], Node | None]:
        def insert(root: Node | None, val: tuple[int, str]) -> Node | None:
            if root is None:
                return Node(val)
            if root.val[0] == val[0]:
                return root
            if root.val[0] < val[0]:
                root.left = insert(root.left, val)
            else:
                root.right = insert(root.right, val)
            return root

        ids = list[tuple[int, str]]()
        for line in input:
            s, _, s_id = line.split()
            ids.append((int(s_id), s))
        root: Node | None = Node(ids[0])
        for id in ids[1:]:
            root = insert(root, id)
        return ids, root

    def part_1(self, input: InputData) -> Output1:
        def getLevel(root: Node | None, target: int, level: int) -> int:
            if root is None:
                return -1
            if root.val[0] == target:
                return level
            leftLevel = getLevel(root.left, target, level + 1)
            if leftLevel != -1:
                return leftLevel
            return getLevel(root.right, target, level + 1)

        blocks = to_blocks(input)
        ids, root = self.parse(blocks[0])
        by_level = defaultdict[int, set[int]](set)
        for id in ids:
            lvl = getLevel(root, id[0], 1)
            by_level[lvl].add(id[0])
        return len(by_level) * max(sum(v) for v in by_level.values())

    def part_2(self, input: InputData) -> Output2:
        blocks = to_blocks(input)
        _, root = self.parse(blocks[0])
        ans = []
        while root:
            ans.append(root.val[1])
            root = root.left if root.val[0] < 500_000 else root.right
        return "-".join(ans)

    def part_3(self, input: InputData) -> Output3:
        def LCA(root: Node | None, n1: Node, n2: Node) -> Node | None:
            if root is None:
                return None
            if root.val[0] > n1.val[0] and root.val[0] > n2.val[0]:
                return LCA(root.right, n1, n2)
            if root.val[0] < n1.val[0] and root.val[0] < n2.val[0]:
                return LCA(root.left, n1, n2)
            return root

        def find(root: Node | None, val: int) -> Node | None:
            if root is None:
                return None
            if root.val[0] == val:
                return root
            elif root.val[0] < val:
                return find(root.left, val)
            else:
                return find(root.right, val)

        blocks = to_blocks(input)
        _, root = self.parse(blocks[0])
        r1 = find(root, int(blocks[1][0].split()[2]))
        r2 = find(root, int(blocks[1][1].split()[2]))
        assert r1 is not None
        assert r2 is not None
        lca = LCA(root, r1, r2)
        assert lca is not None
        return lca.val[1]

    @codyssi_samples(
        (
            ("part_1", TEST, 12645822),
            (
                "part_2",
                TEST,
                "ozNxANO-pYNonIG-MUantNm-lOSlxki-SDJtdpa-JSXfNAJ",
            ),
            ("part_3", TEST, "pYNonIG"),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(19)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
