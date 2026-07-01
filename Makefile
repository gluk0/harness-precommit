.PHONY: bootstrap test lint format validate docker-build docker-run

bootstrap:
	uv pip install -e . && uv run pre-commit install && git submodule update --init

test:
	uv run pytest tests/

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/

validate:
	uv run harness-schema-hook $${FILES}

docker-build:
	docker build -t harness-precommit:local .

docker-run:
	docker run --rm -v $$(pwd):/app harness-precommit:local
