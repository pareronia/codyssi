import operator
import sys
from collections import defaultdict
from functools import cache
from functools import reduce

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples
from codyssi.common import log
from codyssi.common import to_blocks

TEST1 = """\
S1 : 0 -> 6 : FROM START TO END
S2 : 2 -> 3 : FROM S1 TO S1

Possible Moves : 1, 3
"""
TEST2 = """\
S1 : 0 -> 6 : FROM START TO END
S2 : 2 -> 4 : FROM S1 TO S1
S3 : 3 -> 5 : FROM S2 TO S1

Possible Moves : 1, 2
"""
TEST3 = """\
S1 : 0 -> 99 : FROM START TO END
S2 : 8 -> 91 : FROM S1 TO S1
S3 : 82 -> 91 : FROM S1 TO S1
S4 : 90 -> 97 : FROM S2 TO S1
S5 : 29 -> 74 : FROM S1 TO S1
S6 : 87 -> 90 : FROM S3 TO S2
S7 : 37 -> 71 : FROM S2 TO S1
S8 : 88 -> 90 : FROM S6 TO S3
S9 : 34 -> 37 : FROM S2 TO S5
S10 : 13 -> 57 : FROM S1 TO S2

Possible Moves : 1, 3, 5, 6
"""

Output1 = int
Output2 = int
Output3 = str
Step = tuple[int, int]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        @cache
        def count(n: int) -> int:
            if n == 0:
                return 1
            if n < 0:
                return 0
            return sum(count(n - a) for a in allowed)

        blocks = to_blocks(input)
        target = int(blocks[0][0].split()[4])
        allowed = list(map(int, blocks[1][0].split(" : ")[1].split(", ")))
        return count(target)

    def part_2(self, input: InputData) -> Output2:
        @cache
        def count(n: Step) -> int:
            if n == (1, 0):
                return 1
            return sum(
                count(s)
                for s in reduce(operator.ior, (moves(n, a) for a in allowed))
            )

        def moves(n: Step, cnt: int) -> set[Step]:
            def dfs(s: Step, i: int) -> set[Step]:
                if i == 0:
                    return {s}
                return reduce(
                    operator.ior, (dfs(ss, i - 1) for ss in steps[s]), set()
                )

            return dfs(n, cnt)

        blocks = to_blocks(input)
        steps = defaultdict[Step, set[Step]](set)
        for line in blocks[0]:
            ss, _, sstart, _, send, _, _, sstart_s, _, send_s = line.split()
            n, start, end = int(ss[1:]), int(sstart), int(send)
            for i in range(end, start, -1):
                steps[(n, i)].add((n, i - 1))
            if n == 1:
                target = end
                continue
            steps[(int(send_s[1:]), end)].add((n, end))
            steps[(n, start)].add((int(sstart_s[1:]), start))
        # log(steps)
        allowed = list(map(int, blocks[1][0].split(" : ")[1].split(", ")))
        return count((1, target))

    def part_3(self, input: InputData) -> Output3:
        log("hey")
        return ""

    @codyssi_samples(
        (
            ("part_1", TEST1, 6),
            ("part_1", TEST2, 13),
            ("part_1", TEST3, 231843173048269749794),
            ("part_2", TEST1, 17),
            ("part_2", TEST2, 102),
            ("part_2", TEST3, 113524314072255566781694),
            ("part_3", TEST1, "S1_0-S2_2-S2_3-S1_5-S1_6"),
            ("part_3", TEST2, "S1_0-S1_2-S2_3-S3_4-S3_5-S1_6"),
            (
                "part_3",
                TEST3,
                "S1_0-S1_6-S2_11-S2_17-S2_23-S2_29-S9_34-S9_37-S5_42-S5_48-\
                S5_54-S5_60-S5_66-S5_72-S5_73-S5_74-S1_79-S3_84-S8_88-S8_89-\
                S8_90-S3_90-S3_91-S1_96-S1_99",
            ),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(21)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
