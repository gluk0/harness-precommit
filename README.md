# Harness Pipeline Schema Pre-commit Validator

A pre-commit hook to validate Harness pipeline YAML files against the `harness-schema` repository.

## Setup

\`\`\`bash
make bootstrap
\`\`\`

## Usage

Validate files:

\`\`\`bash
make validate FILES="path/to/pipeline.yaml"
\`\`\`

Run tests:

\`\`\`bash
make test
\`\`\`

The pre-commit hook validates YAML files with a top-level \`pipeline\` key.
