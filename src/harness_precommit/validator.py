import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator

DEFAULT_SCHEMA_RELATIVE_PATH = Path("harness-schema/v0/pipeline.json")


class ValidationError(Exception):
    """Raised when schema validation cannot be performed."""


@dataclass(frozen=True)
class ValidationIssue:
    file_path: Path
    document_index: int
    location: str
    message: str


@dataclass(frozen=True)
class FileValidationResult:
    issues: list[ValidationIssue]
    validated_documents: int
    skipped_documents: int


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "harness-schema").exists():
            return candidate
    raise ValidationError("Unable to locate project root containing 'harness-schema'.")


def load_schema(schema_path: Path) -> dict[str, Any]:
    try:
        with schema_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise ValidationError(f"Schema file not found: {schema_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON schema at {schema_path}: {exc}") from exc


def load_yaml_documents(file_path: Path) -> list[Any]:
    with file_path.open("r", encoding="utf-8") as f:
        return list(yaml.safe_load_all(f))


def _normalize_pipeline_document(doc: dict[str, Any]) -> dict[str, Any] | None:
    if "pipeline" in doc:
        return doc

    template = doc.get("template")
    if not isinstance(template, dict):
        return None
    if template.get("type") != "Pipeline":
        return None

    spec = template.get("spec")
    if not isinstance(spec, dict):
        return None

    pipeline_data = {key: value for key, value in template.items() if key not in {"type", "spec"}}
    pipeline_data.update(spec)
    return {"pipeline": pipeline_data}


def validate_yaml_file(file_path: Path, validator: Draft7Validator) -> FileValidationResult:
    issues: list[ValidationIssue] = []
    validated_documents = 0
    skipped_documents = 0

    try:
        docs = load_yaml_documents(file_path)
    except yaml.YAMLError as exc:
        return FileValidationResult(
            issues=[
                ValidationIssue(
                    file_path=file_path,
                    document_index=1,
                    location="<yaml>",
                    message=f"YAML parsing failed: {exc}",
                )
            ],
            validated_documents=0,
            skipped_documents=0,
        )

    if not docs:
        return FileValidationResult(
            issues=[],
            validated_documents=0,
            skipped_documents=0,
        )

    for index, doc in enumerate(docs, start=1):
        if doc is None:
            skipped_documents += 1
            continue
        if not isinstance(doc, dict):
            skipped_documents += 1
            continue

        normalized_doc = _normalize_pipeline_document(doc)
        if normalized_doc is None:
            skipped_documents += 1
            continue

        validated_documents += 1
        for err in validator.iter_errors(normalized_doc):
            location = " -> ".join(str(part) for part in err.path) or "<root>"
            issues.append(
                ValidationIssue(
                    file_path=file_path,
                    document_index=index,
                    location=location,
                    message=err.message,
                )
            )

    return FileValidationResult(
        issues=issues,
        validated_documents=validated_documents,
        skipped_documents=skipped_documents,
    )


def build_validator(schema_path: Path) -> Draft7Validator:
    schema = load_schema(schema_path)
    return Draft7Validator(schema)
