import os


class Table:
    def __init__(self, number_of_problems: int) -> None:
        self.number_of_problems = number_of_problems

    def get_py(self, problem: int) -> str:
        path = os.path.join("src", "main", f"codyssi{problem:02}.py")
        return f"[✓]({path})" if os.path.exists(path) else ""

    def generate(self, file_name: str) -> None:
        url = "https://www.codyssi.com/view_problem_"
        with open(file_name, "r", encoding="utf-8") as f:
            tmp = f.read()
        with open(file_name, "w", encoding="utf-8") as f:
            in_table = False
            for line in tmp.splitlines():
                if line.startswith("<!-- @BEGIN:Problems"):
                    in_table = True
                    print(line, file=f)
                    print("| Problem | python3 |", file=f)
                    print("| --- | --- |", file=f)
                    for problem in range(1, self.number_of_problems + 1):
                        py = self.get_py(problem)
                        line = f"|[{problem}]({url}{problem})|{py}|"
                        print(line, file=f)
                elif line.startswith("<!-- @END:Problems"):
                    in_table = False
                    print(line, file=f)
                else:
                    if not in_table:
                        print(line, file=f)
