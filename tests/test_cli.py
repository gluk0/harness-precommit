from pathlib import Path

from typer.testing import CliRunner

from harness_precommit.cli import app

runner = CliRunner()


def test_cli_fails_on_invalid_pipeline() -> None:
    invalid_fixture = "tests/fixtures/invalid_pipeline.yaml"
    result = runner.invoke(
        app,
        [
            invalid_fixture,
            "--schema-path",
            "harness-schema/v0/pipeline.json",
        ],
    )

    assert result.exit_code == 1
    output = f"{result.stdout}\n{result.stderr}".lower()
    assert "validation failed" in output
    assert invalid_fixture in output


def test_cli_dry_run_returns_success_for_invalid_pipeline() -> None:
    result = runner.invoke(
        app,
        [
            "tests/fixtures/invalid_pipeline.yaml",
            "--schema-path",
            "harness-schema/v0/pipeline.json",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    output = f"{result.stdout}\n{result.stderr}".lower()
    assert "dry run mode enabled" in output


def test_cli_validates_template_based_pipeline_fixture() -> None:
    result = runner.invoke(
        app,
        [
            "tests/fixtures/artefacts/pipelines/service_alpha/v1.0.0.yaml",
            "--schema-path",
            "harness-schema/v0/pipeline.json",
        ],
    )

    assert result.exit_code == 0
    output = f"{result.stdout}\n{result.stderr}".lower()
    assert "1 document(s) validated" in output


def test_cli_succeeds_for_non_pipeline_yaml(tmp_path: Path) -> None:
    sample = tmp_path / "other.yaml"
    sample.write_text("foo: bar\n", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            str(sample),
            "--schema-path",
            "harness-schema/v0/pipeline.json",
        ],
    )

    assert result.exit_code == 0
