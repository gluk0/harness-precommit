FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY . .
RUN uv pip install -e .
ENTRYPOINT ["uv", "run", "harness-schema-hook"]
