import sys
from collections import defaultdict

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples
from codyssi.common import log
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
    def __init__(self, val: int):
        self.val: int = val
        self.left: Node | None = None
        self.right: Node | None = None

    def __repr__(self) -> str:
        return str(self.val)


class Node2:
    def __init__(self, val: tuple[int, str]):
        self.val: tuple[int, str] = val
        self.left: Node2 | None = None
        self.right: Node2 | None = None

    def __repr__(self) -> str:
        return str(self.val)


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        def insert(root: Node | None, val: int) -> Node | None:
            if root is None:
                return Node(val)
            if root.val == val:
                return root
            if root.val < val:
                root.right = insert(root.right, val)
            else:
                root.left = insert(root.left, val)
            return root

        def getLevel(root: Node | None, target: int, level: int) -> int:
            if root is None:
                return -1
            if root.val == target:
                return level
            leftLevel = getLevel(root.left, target, level + 1)
            if leftLevel != -1:
                return leftLevel
            return getLevel(root.right, target, level + 1)

        blocks = to_blocks(input)
        ids = list[int]()
        for line in blocks[0]:
            _, _, s_id = line.split()
            ids.append(int(s_id))
        root: Node | None = Node(ids[0])
        for i in range(1, len(ids)):
            root = insert(root, ids[i])
        by_level = defaultdict[int, set[int]](set)
        for id in ids:
            lvl = getLevel(root, id, 1)
            by_level[lvl].add(id)
        max_sum = max(sum(v) for _, v in by_level.items())
        return max_sum * len(by_level)

    def part_2(self, input: InputData) -> Output2:
        def insert(root: Node2 | None, val: tuple[int, str]) -> Node2 | None:
            if root is None:
                return Node2(val)
            if root.val == val:
                return root
            if root.val < val:
                root.right = insert(root.right, val)
            else:
                root.left = insert(root.left, val)
            return root

        blocks = to_blocks(input)
        ids = list[tuple[int, str]]()
        for line in blocks[0]:
            s, _, s_id = line.split()
            ids.append((int(s_id), s))
        root: Node2 | None = Node2(ids[0])
        r = root
        for i in range(1, len(ids)):
            r = insert(r, ids[i])
        assert root is not None
        ans = []
        while root:
            ans.append(root.val[1])
            if root.val[0] < 500_000:
                root = root.right
            else:
                root = root.left
        return "-".join(ans)

    def part_3(self, input: InputData) -> Output3:
        def LCA(root: Node2 | None, n1: Node2, n2: Node2) -> Node2 | None:
            if root is None:
                return None
            if root.val[0] > n1.val[0] and root.val[0] > n2.val[0]:
                return LCA(root.right, n1, n2)
            if root.val[0] < n1.val[0] and root.val[0] < n2.val[0]:
                return LCA(root.left, n1, n2)
            return root

        def insert2(root: Node2 | None, val: tuple[int, str]) -> Node2 | None:
            if root is None:
                return Node2(val)
            if root.val[0] == val[0]:
                return root
            if root.val[0] < val[0]:
                root.left = insert2(root.left, val)
            else:
                root.right = insert2(root.right, val)
            return root

        def find(root: Node2 | None, val: int) -> Node2 | None:
            if root is None:
                return None
            if root.val[0] == val:
                return root
            elif root.val[0] < val:
                return find(root.left, val)
            else:
                return find(root.right, val)

        log("hey")
        blocks = to_blocks(input)
        ids = list[tuple[int, str]]()
        for line in blocks[0]:
            s, _, s_id = line.split()
            ids.append((int(s_id), s))
        root: Node2 | None = Node2(ids[0])
        v1 = int(blocks[1][0].split()[2])
        v2 = int(blocks[1][1].split()[2])
        log((v1, v2))
        for i in range(1, len(ids)):
            root = insert2(root, ids[i])
        assert root is not None
        log(root)
        r1 = find(root, v1)
        r2 = find(root, v2)
        assert r1 is not None
        assert r2 is not None
        log((r1.val[1], r2.val[1]))
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
