import sys
from collections import defaultdict
from collections import deque
from enum import Enum
from enum import auto
from enum import unique

from codyssi.common import InputData
from codyssi.common import SolutionBase
from codyssi.common import codyssi_samples
from codyssi.common import to_blocks

TEST = """\
Alpha HAS 131
Bravo HAS 804
Charlie HAS 348
Delta HAS 187
Echo HAS 649
Foxtrot HAS 739

FROM Echo TO Foxtrot AMT 328
FROM Charlie TO Bravo AMT 150
FROM Charlie TO Delta AMT 255
FROM Alpha TO Delta AMT 431
FROM Foxtrot TO Alpha AMT 230
FROM Echo TO Foxtrot AMT 359
FROM Echo TO Alpha AMT 269
FROM Delta TO Foxtrot AMT 430
FROM Bravo TO Echo AMT 455
FROM Charlie TO Delta AMT 302
"""

Output1 = int
Output2 = int
Output3 = int
Balances = dict[str, int]
Transaction = tuple[str, str, int]
Debts = defaultdict[str, deque[tuple[int, str]]]


@unique
class Bookkeeping(Enum):
    MODE_1 = auto()
    MODE_2 = auto()
    MODE_3 = auto()

    def do_transaction(
        self, balances: Balances, debts: Debts, transaction: Transaction
    ) -> None:
        snd, rcv, amt = transaction
        match self:
            case Bookkeeping.MODE_1:
                balances[snd] -= amt
                balances[rcv] += amt
            case Bookkeeping.MODE_2:
                lim_amt = min(amt, balances[snd])
                balances[snd] -= lim_amt
                balances[rcv] += lim_amt
            case Bookkeeping.MODE_3:
                lim_amt = min(amt, balances[snd])
                balances[snd] -= lim_amt
                balances[rcv] += lim_amt
                if amt - lim_amt > 0:
                    debts[snd].append((amt - lim_amt, rcv))
                self.settle_debts(balances, debts)

    def settle_debts(self, balances: Balances, debts: Debts) -> None:
        while True:
            for name in (
                name for name in balances if balances[name] and debts[name]
            ):
                while debts[name] and balances[name]:
                    dbt_amt, dbt_rcv = debts[name].popleft()
                    if balances[name] >= dbt_amt:
                        balances[name] -= dbt_amt
                        balances[dbt_rcv] += dbt_amt
                    else:
                        debts[name].appendleft(
                            (dbt_amt - balances[name], dbt_rcv)
                        )
                        balances[dbt_rcv] += balances[name]
                        balances[name] = 0
                else:
                    break
            else:
                break

    def execute(
        self, balances: Balances, transactions: list[Transaction]
    ) -> Balances:
        debts = defaultdict[str, deque[tuple[int, str]]](deque)
        for transaction in transactions:
            self.do_transaction(balances, debts, transaction)
        return balances


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(self, input: InputData) -> tuple[Balances, list[Transaction]]:
        blocks = to_blocks(input)
        balances = dict[str, int]()
        for line in blocks[0]:
            name, _, amt = line.split()
            balances[name] = int(amt)
        transactions = list[Transaction]()
        for line in blocks[1]:
            _, snd, _, rcv, _, amt = line.split()
            transactions.append((snd, rcv, int(amt)))
        return balances, transactions

    def solve(self, input: InputData, mode: Bookkeeping) -> int:
        return sum(sorted(mode.execute(*self.parse(input)).values())[-3:])

    def part_1(self, input: InputData) -> Output1:
        return self.solve(input, Bookkeeping.MODE_1)

    def part_2(self, input: InputData) -> Output2:
        return self.solve(input, Bookkeeping.MODE_2)

    def part_3(self, input: InputData) -> Output3:
        return self.solve(input, Bookkeeping.MODE_3)

    @codyssi_samples(
        (
            ("part_1", TEST, 2870),
            ("part_2", TEST, 2542),
            ("part_3", TEST, 2511),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(13)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
