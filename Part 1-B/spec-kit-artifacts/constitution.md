# Constitution

## Purpose
The project provides deterministic, structured code review findings for software
quality and security evaluation.

## Principles
1. Findings must follow the required JSON shape.
2. Categories and severities are closed enumerations.
3. Line numbers must identify source locations and be positive.
4. Findings and suggestions must be actionable and non-empty.
5. The evaluator must be reproducible and offline-capable.
6. Verification is measured through schema, property, and semantic scores.

## Quality gates
- At least 15 meaningful evaluation cases.
- Aggregate acceptance score of at least 80%.
- A clean source sample must not create false-positive findings.
- Invalid categories, severities, and line numbers must fail validation.
