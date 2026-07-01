# Harness Pipeline Schema Pre-commit Validator

This repository provides a local pre-commit hook to validate Harness pipeline YAML files against the official `harness-schema` repository.

## What this includes

- A Python CLI built with `typer`
- Schema validation using `jsonschema` + `PyYAML`
- Tooling managed with `uv`
- Linting and formatting with `ruff`
- A local pre-commit hook definition
- Docker support for portable validation
- `harness-schema` tracked as a git submodule

## Repository layout

- `harness-schema/`: official schema repo as git submodule
- `src/harness_precommit/`: validator CLI implementation
- `.pre-commit-config.yaml`: local hook wiring
- `Makefile`: common local tasks
- `Dockerfile`: containerized validator runtime

## Quick start

```bash
make bootstrap
```

This will:

- install Python dependencies with `uv`
- install local pre-commit hooks
- initialize/update submodules

## Use in development

Validate selected files manually:

```bash
make validate FILES="path/to/pipeline.yaml"
```

Run hook against all files:

```bash
make precommit-run
```

Run tests:

```bash
make test
```

Run lint:

```bash
make lint
```

Format code:

```bash
make format
```

## Docker usage

Build image:

```bash
make docker-build
```

Run validator in container:

```bash
docker run --rm -v "$PWD":/app harness-precommit:local your-pipeline.yaml
```

## Pre-commit hook behavior

The hook runs:

```bash
uv run harness-schema-hook <staged yaml files>
```

It only reports schema violations for YAML documents that include a top-level `pipeline` key.
