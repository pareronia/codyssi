import itertools
import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST1 = """\
RULE 1: 8x+2y+3z+5a DIVIDE 9 HAS REMAINDER 4 | DEBRIS VELOCITY (0, -1, 0, 1)
RULE 2: 4x+7y+10z+9a DIVIDE 5 HAS REMAINDER 4 | DEBRIS VELOCITY (0, 1, 0, 1)
RULE 3: 6x+3y+7z+3a DIVIDE 4 HAS REMAINDER 1 | DEBRIS VELOCITY (-1, 0, 1, -1)
RULE 4: 3x+11y+11z+3a DIVIDE 2 HAS REMAINDER 1 | DEBRIS VELOCITY (-1, 1, 0, -1)
"""
TEST2 = """\
RULE 1: 8x+10y+3z+5a DIVIDE 9 HAS REMAINDER 4 | DEBRIS VELOCITY (0, -1, 0, 1)
RULE 2: 3x+7y+10z+9a DIVIDE 9 HAS REMAINDER 4 | DEBRIS VELOCITY (0, 1, 0, 1)
RULE 3: 10x+3y+7z+3a DIVIDE 11 HAS REMAINDER 9 | DEBRIS VELOCITY (-1, 0, 1, -1)
RULE 4: 5x+4y+9z+3a DIVIDE 7 HAS REMAINDER 2 | DEBRIS VELOCITY (0, -1, -1, -1)
RULE 5: 3x+11y+11z+3a DIVIDE 3 HAS REMAINDER 1 | DEBRIS VELOCITY (-1, 1, 0, -1)
RULE 6: 4x+6y+7z+3a DIVIDE 8 HAS REMAINDER 6 | DEBRIS VELOCITY (0, -1, 0, -1)
RULE 7: 7x+4y+3z+7a DIVIDE 11 HAS REMAINDER 5 | DEBRIS VELOCITY (0, 1, 0, -1)
RULE 8: 3x+6y+9z+9a DIVIDE 5 HAS REMAINDER 3 | DEBRIS VELOCITY (1, 1, -1, -1)
"""

Output1 = int
Output2 = int
Output3 = int
Position = tuple[int, int, int, int]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def get_debris(
        self,
        input: InputData,
        range_from: Position,
        range_to: Position,
    ) -> list[tuple[Position, Position]]:
        mx, my, mz, ma = range_from
        nx, ny, nz, na = range_to
        ans = list[tuple[Position, Position]]()
        for x, y, z, a in itertools.product(
            range(mx, nx + 1),
            range(my, ny + 1),
            range(mz, nz + 1),
            range(ma, na + 1),
        ):
            for line in input:
                _, _, eq, _, div, _, _, mod, *rest = line.split()
                v = line.partition("(")[2].rpartition(")")[0]
                eq = eq.replace("x", f"*{x}")
                eq = eq.replace("y", f"*{y}")
                eq = eq.replace("z", f"*{z}")
                eq = eq.replace("a", f"*{a}")
                if divmod(eval(eq), int(div))[1] == int(mod):
                    ans.append(((x, y, z, a), tuple(_ for _ in v.split(","))))
        return ans

    def solve_2(
        self,
        debris: list[tuple[Position, Position]],
        range_from: Position,
        range_to: Position,
    ) -> int:
        return 0

    def sample_1(self, input: InputData) -> Output1:
        debris = self.get_debris(input, (0, 0, 0, -1), (2, 2, 4, 1))
        return len(debris)

    def sample_2(self, input: InputData) -> Output2:
        debris = self.get_debris(input, (0, 0, 0, -1), (2, 2, 4, 1))
        return self.solve_2(debris, (0, 0, 0, -1), (2, 2, 4, 1))

    def part_1(self, input: InputData) -> Output1:
        debris = self.get_debris(input, (0, 0, 0, -1), (9, 14, 59, 1))
        return len(debris)

    def part_2(self, input: InputData) -> Output2:
        debris = self.get_debris(input, (0, 0, 0, -1), (9, 14, 59, 1))
        return self.solve_2(debris, (0, 0, 0, -1), (9, 14, 59, 1))

    def part_3(self, input: InputData) -> Output3:
        return 0

    @codyssi_samples(
        (
            # ("sample_1", TEST1, 146),
            # ("part_1", TEST2, 32545),
            ("sample_2", TEST1, 23),
            ("part_2", TEST2, 217),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(22)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
