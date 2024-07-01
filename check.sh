#!/usr/bin/env bash

set -exu -o pipefail

pdm install
pdm run ruff check src/testtools_cli/generator/scaffold_checker.py \
  src/testtools_cli/generator/scaffold_generator.py \
  src/testtools_cli/cli.py
pdm run mypy src/testtools_cli/generator/scaffold_checker.py \
  src/testtools_cli/generator/scaffold_generator.py \
  src/testtools_cli/cli.py \
  --strict
pdm run pytest tests --durations=5 --cov=. --cov-report term
