Part 1B - Semantic Code Review & Refactoring Assistant
Objective
Build an AI-assisted code review system that analyses source code and produces structured review findings.

Supported Categories
Bug
Security
Performance
Style
Maintainability
Example Output
{ "category": "Bug", "severity": "High", "line": 10, "finding": "Possible division by zero", "suggestion": "Validate denominator before division" }

Output Schema
{ "category": string, "severity": string, "line": integer, "finding": string, "suggestion": string }

Structural Invariants
category must be valid
severity must be Low, Medium or High
line must be positive
finding must not be empty
suggestion must not be empty
Guardrails
invalid categories are rejected
invalid line numbers are rejected
findings cannot be blank
Evaluation Dataset
Minimum 15 cases covering:

bug detection
security findings
performance findings
style findings
maintainability findings
edge cases
Acceptance Threshold
80% minimum aggregate score

Required Structure
Part-1B/ ├── spec-kit-artifacts/ ├── src/ ├── tests/ ├── prompts/ ├── evals/ ├── harness/ ├── evidence/

Required Execution Flow
python harness/evaluation_runner.py

The evaluation runner must produce:

schema score
property score
semantic score
aggregate score
PASS/FAIL result