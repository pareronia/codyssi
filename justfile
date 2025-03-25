set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

alias r := run
alias l := lint

source_dir := join(".", "src")
export PYTHONPATH := source_dir
python := if os_family() == "windows" { "python -O" } else { "python3 -O" }

default:
    @just --choose

# Run Problem by number
run problem:
    @{{python}} -m codyssi.runner --problem {{problem}}

# Run all Problems
run-all:
    @{{python}} -m codyssi.runner --all

# Regenerate table
table:
    @{{python}} -m codyssi.table README.md

# Linting: flake8
flake8:
    @echo "Running flake8"
    @flake8 "{{source_dir}}"

# Linting: bandit - security analyzer
bandit:
    @echo "Running bandit"
    @bandit --configfile pyproject.toml --quiet --recursive "{{source_dir}}"

# Linting: vulture - unused code
vulture:
    @echo "Running vulture"
    @vulture "{{source_dir}}"

# Linting: black - code formating
black-check:
    @echo "Running black check"
    @black --quiet --diff --color --check "{{source_dir}}"

# Linting: mypy - type formating
mypy:
    @echo "Running mypy"
    @mypy --no-error-summary "{{source_dir}}"

# Linting: all
lint: flake8 vulture bandit black-check mypy

# git hook
pre-push: lint
