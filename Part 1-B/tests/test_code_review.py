import json
from pathlib import Path

import pytest

from src.code_review_agent import review_source
from harness.schema_validator import validate_review_output
from harness.property_validator import validate_properties


def test_review_schema_for_supported_categories():
    output = review_source("def divide(a, denominator):\n    return a / denominator\n")
    assert validate_review_output(output) == []


@pytest.mark.parametrize(
    ("source", "category"),
    [
        ("return value / 0\n", "Bug"),
        ("result = eval(user_input)\n", "Security"),
        ("for item in items:\n    out.append(item)\n", "Performance"),
        ("enabled = value == True\n", "Style"),
        ("try:\n    run()\nexcept Exception:\n    pass\n", "Maintainability"),
    ],
)
def test_each_supported_category(source, category):
    findings = review_source(source)
    assert any(item["category"] == category for item in findings)


def test_clean_source_has_no_findings():
    assert review_source("def add(a, b):\n    return a + b\n") == []


def test_none_dereference_is_reported():
    findings = review_source("value = None\nreturn value.name\n")
    assert any(item["category"] == "Bug" and item["line"] == 2 for item in findings)


def test_property_invariants():
    output = review_source("cursor.execute(f\"SELECT * FROM users WHERE id={id}\")\n")
    assert validate_properties(output) == []


def test_schema_rejects_invalid_finding():
    invalid = [{"category": "Unknown", "severity": "Critical", "line": 0,
                "finding": "", "suggestion": ""}]
    errors = validate_review_output(invalid)
    assert errors


def test_evaluation_dataset_has_at_least_fifteen_cases():
    path = Path(__file__).resolve().parents[1] / "evals" / "dataset.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert len(data) >= 15
