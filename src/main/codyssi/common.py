from __future__ import annotations

import time
from abc import ABC
from abc import abstractmethod
from enum import Enum
from enum import unique
from typing import Any
from typing import Callable
from typing import Generic
from typing import Iterable
from typing import NamedTuple
from typing import TypeVar
from typing import cast

import pyperclip
from prettyprinter import cpprint

import codyssi.memo as memo
from codyssi.format import fmt_answer
from codyssi.format import fmt_duration
from codyssi.format import fmt_title


def clog(c: Callable[[], object]) -> None:
    if __debug__:
        log(c())


def log(msg: object) -> None:
    if __debug__:
        cpprint(msg)


def to_blocks(inputs: Iterable[str]) -> list[list[str]]:
    blocks = list[list[str]]()
    idx = 0
    blocks.append([])
    for input in inputs:
        if len(input) == 0:
            blocks.append([])
            idx += 1
        else:
            blocks[idx].append(input)
    return blocks


InputData = tuple[str, ...]
OUTPUT1 = TypeVar("OUTPUT1", bound=str | int)
OUTPUT2 = TypeVar("OUTPUT2", bound=str | int)
OUTPUT3 = TypeVar("OUTPUT3", bound=str | int)


class Problem:
    def __init__(self, problem: int):
        self.problem = problem

    def get_input(self) -> tuple[str, ...] | None:
        return memo.get_input(self.problem)


class SolutionBase(ABC, Generic[OUTPUT1, OUTPUT2, OUTPUT3]):
    @unique
    class Part(Enum):

        PART_1 = "1"
        PART_2 = "2"
        PART_3 = "3"

        def __str__(self) -> str:
            return str(self._value_)

    class PartExecution(NamedTuple):
        part: SolutionBase.Part
        answer: Any = None
        duration: int = 0
        no_input: bool = False

        @property
        def duration_as_ms(self) -> float:
            return self.duration / 1_000_000

    def __init__(self, problem: int):
        self.problem = Problem(problem)
        self.callables = {
            SolutionBase.Part.PART_1: self.part_1,
            SolutionBase.Part.PART_2: self.part_2,
            SolutionBase.Part.PART_3: self.part_3,
        }

    @abstractmethod
    def samples(self) -> None:
        pass

    @abstractmethod
    def part_1(self, input: InputData) -> OUTPUT1:
        pass

    @abstractmethod
    def part_2(self, input: InputData) -> OUTPUT2:
        pass

    @abstractmethod
    def part_3(self, input: InputData) -> OUTPUT3:
        pass

    def run_part(self, part: SolutionBase.Part) -> SolutionBase.PartExecution:
        input = self.problem.get_input()
        if input is None:
            return SolutionBase.PartExecution(part, no_input=True)
        else:
            start = time.time()
            answer = self.callables[part](input)
            return SolutionBase.PartExecution(
                part, answer, int((time.time() - start) * 1e9)
            )

    def run(self, main_args: list[str]) -> None:  # noqa E103
        print()
        print(fmt_title(self.problem.problem))
        print()
        if __debug__:
            self.samples()
        for part in SolutionBase.Part:
            result = self.run_part(part)
            if result.no_input:
                print(f"Part {part}: == NO INPUT FOUND ==")
            else:
                if (
                    result.answer is not None
                    and result.answer != ""
                    and result.answer != 0
                ):
                    pyperclip.copy(str(result.answer))
                answer = fmt_answer(result.answer)
                duration = fmt_duration(result.duration_as_ms)
                print(f"Part {part}: {answer}, took {duration}")


F = TypeVar("F", bound=Callable[..., Any])


def codyssi_samples(
    tests: tuple[tuple[str, str, Any], ...],
) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def wrapper(*args: Any) -> Any:
            _self = args[0]
            for test in tests:
                func, _, expected = test
                input_data = tuple(_ for _ in test[1].splitlines())
                actual = getattr(_self, func)(input_data)
                message = (
                    f"FAILED '{func}'. Expected: '{expected}', was: '{actual}'"
                )
                assert actual == expected, message

        return cast(F, wrapper)

    return decorator
