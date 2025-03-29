import importlib
import types
from argparse import ArgumentParser

from ..format import fmt_answer
from ..format import fmt_duration
from ..format import fmt_title
from ..common import SolutionBase


def get_module(problem: int) -> types.ModuleType | None:
    try:
        return importlib.import_module(f"codyssi{problem:0>2}")
    except ModuleNotFoundError:
        return None


def run(day_mod: types.ModuleType) -> None:
    results = [day_mod.solution.run_part(part) for part in SolutionBase.Part]
    title = fmt_title(day_mod.solution.problem.problem)
    answers = " | ".join((fmt_answer(result.answer) for result in results))
    time = fmt_duration(sum(result.duration_as_ms for result in results))
    print(f"{title} : {answers} ({time})")


def main(_main_args: list[str]) -> None:
    parser = ArgumentParser(
        prog="Codyssi", description="Codyssi Problem runner"
    )
    parser.add_argument(
        "-p",
        "--problem",
        type=int,
        nargs=1,
        help="Number of Problem to run.",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Run all Problems",
    )
    args = parser.parse_args()
    if args.all:
        for problem in range(1, 100):
            day_mod = get_module(problem)
            if day_mod is None:
                continue
            run(day_mod)
    else:
        day_mod = get_module(args.problem[0])
        if day_mod is None:
            return
        run(day_mod)


if __name__ == "__main__":
    main([])
