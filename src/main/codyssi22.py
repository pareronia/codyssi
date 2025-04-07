import itertools
import math
import sys
from collections import deque

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
DIRS = {
    (0, 0, 0),
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
}


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
                eq = eq.replace("x", f"*{x}")
                eq = eq.replace("y", f"*{y}")
                eq = eq.replace("z", f"*{z}")
                eq = eq.replace("a", f"*{a}")
                if divmod(eval(eq), int(div))[1] == int(mod):  # nosec
                    vx, vy, vz, va = map(
                        int,
                        line.partition("(")[2].rpartition(")")[0].split(", "),
                    )
                    ans.append(((x, y, z, a), (vx, vy, vz, va)))
        return ans

    def solve_2(
        self,
        debris: list[tuple[Position, Position]],
        range_from: Position,
        range_to: Position,
        exit: Position,
    ) -> int:
        range_x = range_to[0] - range_from[0] + 1
        range_y = range_to[1] - range_from[1] + 1
        range_z = range_to[2] - range_from[2] + 1
        range_a = range_to[3] - range_from[3] + 1
        period = math.lcm(range_x, range_y, range_z, range_a)
        debrises = [
            [
                [
                    [[False for _ in range(period)] for _ in range(range_a)]
                    for _ in range(range_z)
                ]
                for _ in range(range_y)
            ]
            for _ in range(range_x)
        ]
        for i in range(period):
            for d, v in debris:
                x, y, z, a = d
                dx, dy, dz, da = v
                xx = divmod(x + i * dx, range_x)[1]
                yy = divmod(y + i * dy, range_y)[1]
                zz = divmod(z + i * dz, range_z)[1]
                aa = divmod(a + i * da, range_a)[1]
                debrises[xx][yy][zz][aa][i] = True
        q = deque[tuple[Position, int]]()
        q.append(((0, 0, 0, 0), 0))
        seen = set[tuple[Position, int]]()
        time = -1
        while q:
            p, t = q.popleft()
            if p == exit:
                return t
            if time < t:
                time = t
                seen.clear()
            nxt_t = t + 1
            x, y, z, a = p
            for dx, dy, dz in DIRS:
                nx, ny, nz, na = x + dx, y + dy, z + dz, a
                if (
                    range_from[0] <= nx <= range_to[0]
                    and range_from[1] <= ny <= range_to[1]
                    and range_from[2] <= nz <= range_to[2]
                    and not debrises[nx][ny][nz][divmod(na, range_a)[1]][
                        nxt_t % period
                    ]
                    or (nx, ny, nz, na) == (0, 0, 0, 0)
                ):
                    nxt = ((nx, ny, nz, na), nxt_t)
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append(nxt)
        raise RuntimeError

    def solve_3(
        self,
        debris: list[tuple[Position, Position]],
        range_from: Position,
        range_to: Position,
        exit: Position,
    ) -> int:
        range_x = range_to[0] - range_from[0] + 1
        range_y = range_to[1] - range_from[1] + 1
        range_z = range_to[2] - range_from[2] + 1
        range_a = range_to[3] - range_from[3] + 1
        period = math.lcm(range_x, range_y, range_z, range_a)
        debrises = [
            [
                [
                    [[0 for _ in range(period)] for _ in range(range_a)]
                    for _ in range(range_z)
                ]
                for _ in range(range_y)
            ]
            for _ in range(range_x)
        ]
        for i in range(period):
            for d, v in debris:
                x, y, z, a = d
                dx, dy, dz, da = v
                xx = divmod(x + i * dx, range_x)[1]
                yy = divmod(y + i * dy, range_y)[1]
                zz = divmod(z + i * dz, range_z)[1]
                aa = divmod(a + i * da, range_a)[1]
                debrises[xx][yy][zz][aa][i] += 1
        q = deque[tuple[Position, int, int]]()
        q.append(((0, 0, 0, 0), 0, 0))
        seen = set[tuple[Position, int, int]]()
        time = -1
        while q:
            p, t, h = q.popleft()
            if p == exit:
                return t
            if time < t:
                time = t
                seen.clear()
            nxt_t = t + 1
            x, y, z, a = p
            for dx, dy, dz in DIRS:
                nx, ny, nz, na = x + dx, y + dy, z + dz, a
                if (
                    range_from[0] <= nx <= range_to[0]
                    and range_from[1] <= ny <= range_to[1]
                    and range_from[2] <= nz <= range_to[2]
                    and h
                    + debrises[nx][ny][nz][divmod(na, range_a)[1]][
                        nxt_t % period
                    ]
                    <= 3
                    or (nx, ny, nz, na) == (0, 0, 0, 0)
                ):
                    if (nx, ny, nz, na) == (0, 0, 0, 0):
                        nxt = ((0, 0, 0, 0), nxt_t, h)
                    else:
                        nxt = (
                            (nx, ny, nz, na),
                            nxt_t,
                            h
                            + debrises[nx][ny][nz][divmod(na, range_a)[1]][
                                nxt_t % period
                            ],
                        )
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append(nxt)
        raise RuntimeError

    def sample_1(self, input: InputData) -> Output1:
        debris = self.get_debris(input, (0, 0, 0, -1), (2, 2, 4, 1))
        return len(debris)

    def sample_2(self, input: InputData) -> Output2:
        debris = self.get_debris(input, (0, 0, 0, -1), (2, 2, 4, 1))
        return self.solve_2(debris, (0, 0, 0, -1), (2, 2, 4, 1), (2, 2, 4, 0))

    def sample_3(self, input: InputData) -> Output2:
        debris = self.get_debris(input, (0, 0, 0, -1), (2, 2, 4, 1))
        return self.solve_3(debris, (0, 0, 0, -1), (2, 2, 4, 1), (2, 2, 4, 0))

    def part_1(self, input: InputData) -> Output1:
        debris = self.get_debris(input, (0, 0, 0, -1), (9, 14, 59, 1))
        return len(debris)

    def part_2(self, input: InputData) -> Output2:
        debris = self.get_debris(input, (0, 0, 0, -1), (9, 14, 59, 1))
        return self.solve_2(
            debris, (0, 0, 0, -1), (9, 14, 59, 1), (9, 14, 59, 0)
        )

    def part_3(self, input: InputData) -> Output3:
        debris = self.get_debris(input, (0, 0, 0, -1), (9, 14, 59, 1))
        return self.solve_3(
            debris, (0, 0, 0, -1), (9, 14, 59, 1), (9, 14, 59, 0)
        )

    @codyssi_samples(
        (
            ("sample_1", TEST1, 146),
            ("part_1", TEST2, 32545),
            ("sample_2", TEST1, 23),
            ("part_2", TEST2, 217),
            ("sample_3", TEST1, 8),
            ("part_3", TEST2, 166),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(22)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
