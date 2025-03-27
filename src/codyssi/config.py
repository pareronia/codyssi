import tomllib
from typing import cast


class Config:

    def __init__(self, toml: str) -> None:
        with open(toml, "rb") as f:
            self.dict = tomllib.load(f)

    def get_number_of_problems(self) -> int:
        return cast(
            int, self.dict["tool"]["codyssi"]["table"]["number_of_problems"]
        )
