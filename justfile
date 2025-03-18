alias r := run
alias l := lint

default:
    @just --choose

run problem:
    @python3 -O $(printf "codyssi%02d.py" {{problem}})

run-all:
    @find {{invocation_directory()}} -name "codyssi*.py" -exec python3 -O {} \;

table:
    @python3 -m codyssi.table README.md

flake8:
    @echo "Running flake"
    @flake8 {{invocation_directory()}}

bandit:
    @echo "Running bandit"
    @bandit --configfile pyproject.toml --quiet --recursive {{invocation_directory()}}

vulture:
    @echo "Running vulture"
    @vulture {{invocation_directory()}}

black-check:
    @echo "Running black check"
    @black --quiet --diff --color --check {{invocation_directory()}}

mypy:
    @echo "Running mypy"
    @mypy --no-error-summary {{invocation_directory()}}

lint: flake8 vulture bandit black-check mypy

pre-push: lint
