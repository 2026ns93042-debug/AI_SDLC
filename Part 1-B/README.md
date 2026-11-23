# Semantic Code Review & Refactoring Assistant

This project provides an offline, deterministic Python code-review assistant.
It detects sample bug, security, performance, style, and maintainability issues
and returns findings in the required structured schema.

## Run the evaluation

```powershell
python harness/evaluation_runner.py
```

The command prints:

- Schema score
- Property score
- Semantic score
- Aggregate score
- PASS/FAIL result

It writes a complete machine-readable report to:

`evidence/evaluation_report.json`

## Run tests

```powershell
python -m pytest -q
```

## Project layout

- `src/code_review_agent.py`: source analysis implementation
- `prompts/review_prompt.txt`: structured review instructions
- `evals/dataset.json`: evaluation cases
- `harness/`: schema, property, semantic, and runner modules
- `spec-kit-artifacts/`: constitution and implementation specifications
- `tests/test_code_review.py`: focused unit tests
- `evidence/`: generated evaluation evidence

## Review API

```python
from src.code_review_agent import review_source

findings = review_source("def divide(a, b):\n    return a / b\n")
```

Every finding contains `category`, `severity`, `line`, `finding`, and `suggestion`.
