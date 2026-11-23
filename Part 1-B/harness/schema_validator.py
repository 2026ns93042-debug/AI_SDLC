"""Validate structured code review findings."""

from typing import Iterable

VALID_CATEGORIES = {"Bug", "Security", "Performance", "Style", "Maintainability"}
VALID_SEVERITIES = {"Low", "Medium", "High"}
REQUIRED_FIELDS = {"category", "severity", "line", "finding", "suggestion"}


def validate_finding(finding: object) -> list[str]:
    if not isinstance(finding, dict):
        return ["finding must be an object"]

    errors = []
    missing = REQUIRED_FIELDS - finding.keys()
    if missing:
        errors.append("missing fields: " + ", ".join(sorted(missing)))
    if finding.get("category") not in VALID_CATEGORIES:
        errors.append("invalid category")
    if finding.get("severity") not in VALID_SEVERITIES:
        errors.append("invalid severity")
    line = finding.get("line")
    if not isinstance(line, int) or isinstance(line, bool) or line <= 0:
        errors.append("line must be a positive integer")
    if not isinstance(finding.get("finding"), str) or not finding["finding"].strip():
        errors.append("finding must not be blank")
    if not isinstance(finding.get("suggestion"), str) or not finding["suggestion"].strip():
        errors.append("suggestion must not be blank")
    return errors


def validate_review_output(output: object) -> list[str]:
    if not isinstance(output, list):
        return ["review output must be a list"]
    errors = []
    for index, finding in enumerate(output):
        for error in validate_finding(finding):
            errors.append(f"finding {index}: {error}")
    return errors


def schema_score(results: Iterable[object]) -> float:
    results = list(results)
    if not results:
        return 0.0
    valid = sum(not validate_review_output(result) for result in results)
    return valid / len(results)
