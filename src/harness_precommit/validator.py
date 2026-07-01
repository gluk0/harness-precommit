import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError

def load_schema(schema_path):
    with open(schema_path) as f:
        return json.load(f)

def validate_yaml(yaml_path, schema_path):
    with open(yaml_path) as f:
        doc = yaml.safe_load(f)
    schema = load_schema(schema_path)
    validate(instance=doc, schema=schema)
