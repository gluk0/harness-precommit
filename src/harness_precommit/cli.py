import typer
from .validator import validate_yaml

app = typer.Typer()

@app.command()
def validate(files: list[str]):
    """Validate pipeline YAML files against schema"""
    for f in files:
        print(f"Validating {f}...")
