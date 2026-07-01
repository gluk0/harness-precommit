import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError as JSONSchemaError

def get_schema_path():
    return Path(__file__).parent / "schemas" / "pipeline_schema.json"

def load_schema(schema_path):
    with open(schema_path) as f:
        return json.load(f)

def validate_yaml(yaml_path, schema=None):
    with open(yaml_path) as f:
        doc = yaml.safe_load(f)
    
    if schema is None:
        schema = load_schema(get_schema_path())
    
    if "pipeline" not in doc:
        return
    
    validate(instance=doc, schema=schema)
