import itertools
import operator
import sys
from enum import Enum
from enum import auto
from enum import unique
from typing import Callable

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples
from codyssi.common import to_blocks

TEST = """\
222 267 922 632 944
110 33 503 758 129
742 697 425 362 568
833 408 425 349 631
874 671 202 430 602

SHIFT COL 2 BY 1
MULTIPLY 4 COL 5
SUB 28 ALL
SHIFT COL 4 BY 2
MULTIPLY 4 ROW 4
ADD 26 ROW 3
SHIFT COL 4 BY 2
ADD 68 ROW 2

TAKE
CYCLE
TAKE
ACT
TAKE
CYCLE
"""

Output1 = int
Output2 = int
Output3 = int
OPERATORS = {
    "ADD": operator.add,
    "SUB": operator.sub,
    "MULTIPLY": operator.mul,
}
MOD = 1073741824


@unique
class FlowsRounds(Enum):
    NONE = auto()
    ONCE = auto()
    ALL = auto()


class Solution(SolutionBase[Output1, Output2, Output3]):

    def solve(self, input: InputData, flows_rounds: FlowsRounds) -> int:
        def execute(grid: list[list[int]], instruction: str) -> None:
            def op(
                r: int, c: int, operator: Callable[[int, int], int], amt: int
            ) -> None:
                grid[r][c] = operator(grid[r][c], amt) % MOD

            size = len(grid)
            words = instruction.split()
            if words[0] == "SHIFT":
                idx = int(words[2]) - 1
                amt = int(words[4])
                match words[1]:
                    case "ROW":
                        grid[idx] = [
                            grid[idx][(i - amt) % size] for i in range(size)
                        ]
                    case "COL":
                        col = [grid[row][idx] for row in range(size)]
                        tmp = [col[(i - amt) % size] for i in range(size)]
                        for r in range(size):
                            grid[r][idx] = tmp[r]
            else:
                operator = OPERATORS[words[0]]
                amt = int(words[1])
                if words[2] == "ALL":
                    for r, c in itertools.product(range(size), range(size)):
                        op(r, c, operator, amt)
                else:
                    idx = int(words[3]) - 1
                    match words[2]:
                        case "ROW":
                            for c in range(size):
                                op(idx, c, operator, amt)
                        case "COL":
                            for r in range(size):
                                op(r, idx, operator, amt)

        blocks = to_blocks(input)
        grid = [list(map(int, line.split())) for line in blocks[0]]
        if flows_rounds == FlowsRounds.NONE:
            actions = ["ACT"] * len(blocks[1])
        else:
            actions = [_ for _ in blocks[2][1::2]]
        while True:
            for action in actions:
                match action:
                    case "ACT":
                        execute(grid, blocks[1].pop(0))
                    case "CYCLE":
                        blocks[1].append(blocks[1].pop(0))
                if len(blocks[1]) == 0:
                    break
            else:
                if flows_rounds == FlowsRounds.ALL:
                    continue
            break
        return max(
            sum(grid[r][c] for r, c in rc)
            for rc in itertools.chain(
                (((r, c) for c in range(len(grid))) for r in range(len(grid))),
                (((r, c) for r in range(len(grid))) for c in range(len(grid))),
            )
        )

    def part_1(self, input: InputData) -> Output1:
        return self.solve(input, FlowsRounds.NONE)

    def part_2(self, input: InputData) -> Output2:
        return self.solve(input, FlowsRounds.ONCE)

    def part_3(self, input: InputData) -> Output3:
        return self.solve(input, FlowsRounds.ALL)

    @codyssi_samples(
        (
            ("part_1", TEST, 18938),
            ("part_2", TEST, 11496),
            ("part_3", TEST, 19022),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(16)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
