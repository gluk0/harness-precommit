FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
COPY tests ./tests
COPY harness-schema ./harness-schema
COPY .pre-commit-config.yaml ./

RUN uv sync --dev

ENTRYPOINT ["uv", "run", "harness-schema-hook"]
