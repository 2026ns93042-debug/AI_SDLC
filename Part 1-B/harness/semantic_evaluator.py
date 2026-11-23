"""Semantic quality evaluator for code review results."""

from typing import Iterable


def evaluate_case(output: list[dict], expected: dict) -> float:
    if not isinstance(output, list):
        return 0.0

    if expected.get("no_findings"):
        return 1.0 if not output else 0.0

    category = expected["category"]
    matches = [finding for finding in output if finding.get("category") == category]
    if not matches:
        return 0.0

    finding = matches[0]
    score = 0.55

    expected_severity = expected.get("severity")
    if expected_severity and finding.get("severity") == expected_severity:
        score += 0.15

    expected_line = expected.get("line")
    if expected_line and finding.get("line") == expected_line:
        score += 0.15

    finding_text = str(finding.get("finding", "")).lower()
    contains = expected.get("finding_contains")
    if contains and any(term.lower() in finding_text for term in contains):
        score += 0.075

    suggestion_text = str(finding.get("suggestion", "")).lower()
    suggestion_terms = expected.get("suggestion_contains")
    if suggestion_terms and any(term.lower() in suggestion_text for term in suggestion_terms):
        score += 0.075

    return min(score, 1.0)


def semantic_score(results: Iterable[tuple[list[dict], dict]]) -> float:
    results = list(results)
    if not results:
        return 0.0
    return sum(evaluate_case(output, expected) for output, expected in results) / len(results)
