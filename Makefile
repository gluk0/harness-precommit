UV ?= uv

.PHONY: bootstrap lock lint format test validate precommit-run docker-build docker-validate \
        run-valid run-invalid run-all run-invalid-dry-run test-fixtures test-fixtures-dry-run

bootstrap:
	$(UV) sync --dev
	$(UV) run pre-commit install
	git submodule update --init --recursive

lock:
	$(UV) lock

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

test:
	$(UV) run pytest -q

validate:
	$(UV) run harness-schema-hook $(FILES)

precommit-run:
	$(UV) run pre-commit run --all-files

# Validate all valid pipeline fixtures (should all pass)
run-valid:
	@echo "Validating valid pipeline fixtures..."
	$(UV) run harness-schema-hook tests/fixtures/artefacts/pipelines/valid/**/*.yaml
	@echo "✓ All valid fixtures passed"

# Validate all invalid pipeline fixtures (expected to fail)
run-invalid:
	@echo "Validating invalid pipeline fixtures (expected to fail)..."
	$(UV) run harness-schema-hook tests/fixtures/artefacts/pipelines/invalid/**/*.yaml; \
	if [ $$? -eq 1 ]; then \
		echo "✓ Invalid fixtures correctly rejected"; \
	else \
		echo "✗ Invalid fixtures should have failed"; \
		exit 1; \
	fi

# Validate all pipeline and template fixtures
run-all: run-valid run-invalid
	@echo "✓ All fixture validation completed"

# Validate invalid fixtures in dry-run mode (reports issues without failing)
run-invalid-dry-run:
	@echo "Validating invalid pipeline fixtures (dry-run mode)..."
	$(UV) run harness-schema-hook --dry-run tests/fixtures/artefacts/pipelines/invalid/**/*.yaml
	@echo "✓ Dry-run completed (issues reported without exit code 1)"

# Validate all fixtures including templates
test-fixtures:
	@echo "Validating all fixtures..."
	$(UV) run harness-schema-hook tests/fixtures/artefacts/pipelines/**/*.yaml tests/fixtures/artefacts/pipeline-templates/**/*.yaml

# Validate all fixtures in dry-run mode (reports issues without failing)
test-fixtures-dry-run:
	@echo "Validating all fixtures (dry-run mode)..."
	$(UV) run harness-schema-hook --dry-run tests/fixtures/artefacts/pipelines/**/*.yaml tests/fixtures/artefacts/pipeline-templates/**/*.yaml

docker-build:
	docker build -t harness-precommit:local .

docker-validate:
	docker run --rm -v $(PWD):/app harness-precommit:local harness-schema/v0/pipeline/examples/conditional-retry-example.yaml

docker-build:
	docker build -t harness-precommit:local .

docker-run:
	docker run --rm -v $$(pwd):/app harness-precommit:local
