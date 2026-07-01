from collections import defaultdict
from pathlib import Path

import typer

from harness_precommit.validator import (
    DEFAULT_SCHEMA_RELATIVE_PATH,
    FileValidationResult,
    ValidationError,
    ValidationIssue,
    build_validator,
    find_project_root,
    validate_yaml_file,
)

app = typer.Typer(help="Validate Harness pipeline YAML files against local harness-schema.")


@app.command()
def validate(
    files: list[Path] = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    schema_path: Path | None = typer.Option(
        None,
        "--schema-path",
        help="Optional path to pipeline schema JSON. Defaults to harness-schema/v0/pipeline.json.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Report validation results without failing with a non-zero exit code.",
    ),
) -> None:
    """Validate one or more YAML files against the Harness pipeline schema."""
    try:
        root = find_project_root(Path.cwd())
        effective_schema_path = (
            (root / DEFAULT_SCHEMA_RELATIVE_PATH) if schema_path is None else schema_path
        )
        validator = build_validator(effective_schema_path)
    except ValidationError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    all_results: list[FileValidationResult] = []
    for file_path in files:
        if file_path.suffix.lower() not in {".yaml", ".yml"}:
            continue
        all_results.append(validate_yaml_file(file_path, validator))

    all_issues: list[ValidationIssue] = []
    validated_docs = 0
    skipped_docs = 0
    for result in all_results:
        all_issues.extend(result.issues)
        validated_docs += result.validated_documents
        skipped_docs += result.skipped_documents

    if all_issues:
        typer.secho("Harness pipeline schema validation failed:", fg=typer.colors.RED, err=True)
        issues_by_file: dict[Path, list[ValidationIssue]] = defaultdict(list)
        for issue in all_issues:
            issues_by_file[issue.file_path].append(issue)

        for file_path, issues in issues_by_file.items():
            typer.secho(f"\nFile: {file_path}", fg=typer.colors.YELLOW, err=True)
            for issue in issues:
                typer.echo(
                    f"  [doc {issue.document_index}] at {issue.location}: {issue.message}",
                    err=True,
                )

        typer.secho(
            (
                f"\nSummary: {len(all_issues)} error(s), "
                f"{validated_docs} document(s) validated, {skipped_docs} skipped."
            ),
            fg=typer.colors.RED,
            err=True,
        )
        if dry_run:
            typer.secho("Dry run mode enabled: returning success for review.", fg=typer.colors.BLUE)
            return
        raise typer.Exit(code=1)

    typer.secho(
        (
            "Harness pipeline schema validation passed. "
            f"({validated_docs} document(s) validated, {skipped_docs} skipped)"
        ),
        fg=typer.colors.GREEN,
    )


if __name__ == "__main__":
    app()
