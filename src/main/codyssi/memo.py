import json
import os
import sys

from . import CODYSSI_DIR
from . import CODYSSI_TOKEN


def get_codyssi_dir() -> str:
    if CODYSSI_DIR in os.environ:
        return os.environ[CODYSSI_DIR]
    if sys.platform.startswith("win"):
        return os.path.join(os.environ["APPDATA"], "codyssi")
    if sys.platform.startswith("linux"):
        return os.path.join(os.environ["HOME"], ".config", "codyssi")
    raise RuntimeError("OS not supported")


def get_token() -> str:
    if CODYSSI_TOKEN in os.environ:
        return os.environ[CODYSSI_TOKEN]
    file = os.path.join(get_codyssi_dir(), "token")
    return read_lines_from_file(file)[0]


def get_user_id(token: str) -> str:
    file = os.path.join(get_codyssi_dir(), "token2id.json")
    with open(file, "r", encoding="utf-8") as f:
        ids = json.load(f)
    return str(ids[token])


def get_memo_dir() -> str:
    return os.path.join(get_codyssi_dir(), get_user_id(get_token()))


def get_input_file(problem: int) -> str:
    return os.path.join(get_memo_dir(), f"{problem:>02}_input.txt")


def get_input(problem: int) -> tuple[str, ...] | None:
    file = get_input_file(problem)
    if not os.path.exists(file):
        return None
    return tuple(_ for _ in read_lines_from_file(file))


def get_answer_file(problem: int, part: int) -> str:
    return os.path.join(get_memo_dir(), f"{problem:>02}_{part}_answer.txt")


def get_answer(problem: int, part: int) -> str | None:
    file = get_answer_file(problem, part)
    if not os.path.exists(file):
        return None
    lines = read_lines_from_file(file)
    if len(lines) == 0:
        return None
    return lines[0]


def read_lines_from_file(file: str) -> list[str]:
    with open(file, "r", encoding="utf-8") as f:
        data = f.read()
    return data.rstrip("\r\n").splitlines()
