import typer
from pathlib import Path
from .validator import validate_yaml, ValidationError

app = typer.Typer()

@app.command()
def validate(files: list[str]):
    """Validate pipeline YAML files against schema"""
    errors = []
    for f in files:
        try:
            validate_yaml(f, str(Path(__file__).parent / "schema.json"))
        except ValidationError as e:
            errors.append(f"{f}: {e.message}")
    if errors:
        for err in errors:
            print(err)
        raise typer.Exit(1)
