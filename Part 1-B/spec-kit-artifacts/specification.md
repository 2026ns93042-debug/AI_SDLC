# Specification

## Goal
Build an AI-assisted code review system that analyses source code and emits
structured findings across Bug, Security, Performance, Style, and Maintainability.

## Output contract
Each finding is an object containing:

- `category`: one of Bug, Security, Performance, Style, Maintainability
- `severity`: Low, Medium, or High
- `line`: positive integer
- `finding`: non-empty string
- `suggestion`: non-empty string

## Functional requirements
1. Detect clear bug, security, performance, style, and maintainability patterns.
2. Return a JSON-compatible list of findings.
3. Validate every finding against the structural contract.
4. Evaluate semantic relevance against an expected finding.
5. Produce a single aggregate PASS/FAIL result.

## Acceptance criteria
- The evaluation runner executes with Python.
- All three component scores and the aggregate score are printed.
- PASS is produced at aggregate score >= 80%.
- The report is persisted under `evidence/`.
