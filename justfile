alias r := run
alias l := lint

source_dir := justfile_directory() + "/src"
pythonpath := "PYTHONPATH=" + source_dir
python3 := "python3 -O"

default:
    @just --choose

run problem:
    @{{python3}} {{source_dir}}/$(printf "codyssi%02d.py" {{problem}})

run-all:
    @find {{source_dir}} -name "codyssi*.py" -exec {{python3}} {} \;

table:
    @{{pythonpath}} {{python3}} -m codyssi.table README.md

flake8:
    @echo "Running flake"
    @flake8 {{source_dir}}

bandit:
    @echo "Running bandit"
    @bandit --configfile pyproject.toml --quiet --recursive {{source_dir}}

vulture:
    @echo "Running vulture"
    @vulture {{source_dir}}

black-check:
    @echo "Running black check"
    @black --quiet --diff --color --check {{source_dir}}

mypy:
    @echo "Running mypy"
    @mypy --no-error-summary {{source_dir}}

lint: flake8 vulture bandit black-check mypy

pre-push: lint
