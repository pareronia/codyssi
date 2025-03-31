set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

alias l := lint
alias r := run-all
alias t := test

source_dir := join(".", "src", "main")
test_dir := join(".", "src", "test")
export PYTHONPATH := source_dir
python := if os_family() == "windows" { "python -O" } else { "python3 -O" }
python_dev := if os_family() == "windows" { "python" } else { "python3" }

default:
    @just --choose

# Run Problem by number
run problem:
    @echo {{CLEAR}}
    @{{python}} -m codyssi.runner --problem {{problem}}

# Run all Problems
run-all:
    @echo {{CLEAR}}
    @{{python}} -m codyssi.runner --all

# Run tests
test:
    @echo {{CLEAR}}
    @{{python}} -m unittest discover -s "{{test_dir}}"

# Regenerate table
table:
    @{{python}} -m codyssi.table README.md && git diff README.md

[group("vim")]
vim-file-run-dev file $LOGLEVEL="DEBUG":
    @echo {{CLEAR}}
    @{{python_dev}} "{{file}}"

[group("vim")]
vim-file-run file:
    @echo {{CLEAR}}
    @{{python}} "{{file}}"

[group("vim")]
vim-file-debug file:
    @echo {{CLEAR}}
    @{{python_dev}} -m pdb "{{file}}"

# Linting: flake8
[group("linting")]
flake8:
    @echo "Running flake8"
    @flake8 "{{source_dir}}"

# Linting: bandit - security analyzer
[group("linting")]
bandit:
    @echo "Running bandit"
    @bandit --configfile pyproject.toml --quiet --recursive "{{source_dir}}"

# Linting: vulture - unused code
[group("linting")]
vulture:
    @echo "Running vulture"
    @vulture "{{source_dir}}"

# Linting: black - code formating
[group("linting")]
black-check:
    @echo "Running black check"
    @black --quiet --diff --color --check "{{source_dir}}"

# Linting: mypy - type formating
[group("linting")]
mypy:
    @echo "Running mypy"
    @mypy --no-error-summary "{{source_dir}}"

# Linting: all
[group("linting")]
lint: flake8 vulture bandit black-check mypy

# git hook
pre-push: lint test
