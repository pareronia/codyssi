import itertools
import math
import sys
from collections import deque

from codyssi.common import InputData
from codyssi.common import SolutionBase2

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

Position = tuple[int, int, int, int]
Debris = list[tuple[Position, Position]]
Debrises = list[list[list[list[list[int]]]]]
Space = tuple[Position, Position]
Input = tuple[Debris, Debrises]
Output1 = int
Output2 = int
Output3 = int
DIRS = {
    (0, 0, 0),
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
}
START = (0, 0, 0, 0)
SAMPLE_EXIT = (2, 2, 4, 0)
EXIT = (9, 14, 59, 0)
SAMPLE_SPACE = ((0, 0, 0, -1), (2, 2, 4, 1))
SPACE = ((0, 0, 0, -1), (9, 14, 59, 1))


class Solution(SolutionBase2[Input, Output1, Output2, Output3]):
    def get_debris(self, input: InputData, space: Space) -> Debris:
        ans = Debris()
        for x, y, z, a in itertools.product(
            range(space[0][0], space[1][0] + 1),
            range(space[0][1], space[1][1] + 1),
            range(space[0][2], space[1][2] + 1),
            range(space[0][3], space[1][3] + 1),
        ):
            for line in input:
                _, _, eq, _, div, _, _, mod, *rest = line.split()
                fx, fy, fz, fa = map(lambda sp: int(sp[:-1]), eq.split("+"))
                if (fx * x + fy * y + fz * z + fa * a) % int(div) == int(mod):
                    vx, vy, vz, va = map(
                        int,
                        line.partition("(")[2].rpartition(")")[0].split(", "),
                    )
                    ans.append(((x, y, z, a), (vx, vy, vz, va)))
        return ans

    def get_debrises(self, debris: Debris, space: Space) -> Debrises:
        range_x = space[1][0] - space[0][0] + 1
        range_y = space[1][1] - space[0][1] + 1
        range_z = space[1][2] - space[0][2] + 1
        range_a = space[1][3] - space[0][3] + 1
        period = math.lcm(range_x, range_y, range_z, range_a)
        debrises = [
            [
                [
                    [[0 for _ in range(period)] for _ in range(range_z)]
                    for _ in range(range_y)
                ]
                for _ in range(range_x)
            ]
            for _ in range(range_a)
        ]
        for i in range(period):
            for d, v in debris:
                x, y, z, a = d
                dx, dy, dz, da = v
                xx = (x + i * dx) % range_x
                yy = (y + i * dy) % range_y
                zz = (z + i * dz) % range_z
                aa = divmod(a + i * da, range_a)[1]
                debrises[aa][xx][yy][zz][i] += 1
        return debrises

    def get_lowest_duration(
        self,
        debrises: Debrises,
        space: Space,
        exit: Position,
        acceptable_hits: int,
    ) -> int:
        period = len(debrises[0][0][0][0])
        start, end = START[:3], exit[:3]
        min_x, max_x = space[0][0], space[1][0]
        min_y, max_y = space[0][1], space[1][1]
        min_z, max_z = space[0][2], space[1][2]
        q = deque[tuple[tuple[int, int, int], int, int]]()
        q.append(((start), 0, 0))
        seen = set[tuple[tuple[int, int, int], int, int]]()
        time = -1
        while q:
            p, t, h = q.popleft()
            if p == end:
                return t
            if time < t:
                time = t
                seen.clear()
            nxt_t = t + 1
            x, y, z = p
            for dx, dy, dz in DIRS:
                nx, ny, nz = x + dx, y + dy, z + dz
                if (
                    min_x <= nx <= max_x
                    and min_y <= ny <= max_y
                    and min_z <= nz <= max_z
                ):
                    if (nx, ny, nz) == start:
                        nxt = (start, nxt_t, h)
                    else:
                        nxt_h = h + debrises[0][nx][ny][nz][nxt_t % period]
                        if nxt_h > acceptable_hits:
                            continue
                        nxt = ((nx, ny, nz), nxt_t, nxt_h)
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append(nxt)
        raise RuntimeError

    def parse_input(self, input: InputData) -> Input:
        debris = self.get_debris(input, SPACE)
        return debris, self.get_debrises(debris, SPACE)

    def solve_1(self, debris: Debris, space: Space) -> int:
        return len(debris)

    def solve_2(self, debrises: Debrises, space: Space, exit: Position) -> int:
        return self.get_lowest_duration(
            debrises, space, exit, acceptable_hits=0
        )

    def solve_3(self, debrises: Debrises, space: Space, exit: Position) -> int:
        return self.get_lowest_duration(
            debrises, space, exit, acceptable_hits=3
        )

    def part_1(self, input: Input) -> Output1:
        return self.solve_1(input[0], SPACE)

    def part_2(self, input: Input) -> Output2:
        return self.solve_2(input[1], SPACE, EXIT)

    def part_3(self, input: Input) -> Output3:
        return self.solve_3(input[1], SPACE, EXIT)

    def samples(self) -> None:
        debris = self.get_debris(tuple(TEST1.splitlines()), SAMPLE_SPACE)
        debrises = self.get_debrises(debris, SAMPLE_SPACE)
        assert self.solve_1(debris, SAMPLE_SPACE) == 146
        assert self.solve_2(debrises, SAMPLE_SPACE, SAMPLE_EXIT) == 23
        assert self.solve_3(debrises, SAMPLE_SPACE, SAMPLE_EXIT) == 8
        debris = self.get_debris(tuple(TEST2.splitlines()), SPACE)
        debrises = self.get_debrises(debris, SPACE)
        assert self.solve_1(debris, SPACE) == 32545
        assert self.solve_2(debrises, SPACE, EXIT) == 217
        assert self.solve_3(debrises, SPACE, EXIT) == 166


solution = Solution(22)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
