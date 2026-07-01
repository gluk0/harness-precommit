import typer
import sys
from pathlib import Path
from .validator import validate_yaml, ValidationError as JSONSchemaError

app = typer.Typer(help="Harness pipeline schema validator")

@app.command()
def validate(files: list[str] = typer.Argument(..., help="YAML files to validate")):
    """Validate pipeline YAML files against schema"""
    errors = []
    for f in files:
        try:
            validate_yaml(f)
            print(f"✓ {f}")
        except JSONSchemaError as e:
            errors.append(f"{f}: {e.message}")
        except Exception as e:
            errors.append(f"{f}: {str(e)}")
    
    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for err in errors:
            print(f"  ✗ {err}", file=sys.stderr)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
