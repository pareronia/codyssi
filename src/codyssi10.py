import sys

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples

TEST = """\
t#UD$%%DVd*L?^p?S$^@#@@$pF$?xYJ$LLv$@%EXO&$*iSFZuT!^VMHy#zKISHaBj?e*#&yRVdemc#?&#Q%j&ev*#YWRi@?mNQ@eK
"""

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def values(self, line: str, total: bool) -> list[int]:
        ans = list[int]()
        for ch in line:
            if ch.isalnum():
                ans.append(
                    ord(ch) - ord("a") + 1
                    if ch.islower()
                    else ord(ch) - ord("A") + 27
                )
            elif total:
                ans.append((ans[-1] * 2 - 5 + 52) % 52)
        return ans

    def part_1(self, input: InputData) -> Output1:
        return len(self.values(input[0], total=False))

    def part_2(self, input: InputData) -> Output2:
        return sum(self.values(input[0], total=False))

    def part_3(self, input: InputData) -> Output3:
        return sum(self.values(input[0], total=True))

    @codyssi_samples(
        (
            ("part_1", TEST, 59),
            ("part_2", TEST, 1742),
            ("part_3", TEST, 2708),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(10)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
