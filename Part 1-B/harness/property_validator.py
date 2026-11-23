"""Check structural and behavioral invariants for review findings."""

from typing import Iterable

from harness.schema_validator import validate_review_output


def validate_properties(output: object) -> list[str]:
    errors = validate_review_output(output)
    if not isinstance(output, list):
        return errors
    for index, finding in enumerate(output):
        category = finding.get("category")
        severity = finding.get("severity")
        line = finding.get("line")
        if category in {"Security", "Bug"} and severity not in {"Medium", "High"}:
            errors.append(f"finding {index}: high-impact category needs an appropriate severity")
        if line is not None and (not isinstance(line, int) or isinstance(line, bool) or line <= 0):
            errors.append(f"finding {index}: property line violation")
    return sorted(set(errors))


def property_score(outputs: Iterable[object]) -> float:
    outputs = list(outputs)
    if not outputs:
        return 0.0
    valid = sum(not validate_properties(output) for output in outputs)
    return valid / len(outputs)
