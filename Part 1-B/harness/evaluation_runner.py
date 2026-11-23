"""Run the code review evaluation suite."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.code_review_agent import review_source
from harness.schema_validator import schema_score
from harness.property_validator import property_score
from harness.semantic_evaluator import semantic_score


AGGREGATE_THRESHOLD = 0.80


def main() -> int:
    dataset_path = ROOT / "evals" / "dataset.json"
    with dataset_path.open(encoding="utf-8") as handle:
        dataset = json.load(handle)

    schema_outputs = []
    semantic_results = []
    per_case = []

    for case in dataset:
        output = review_source(case["source"])
        schema_outputs.append(output)
        semantic_results.append((output, case["expected"]))

        expected = case["expected"]
        matching = [item for item in output if item["category"] == expected["category"]]
        per_case.append({
            "id": case["id"],
            "name": case["name"],
            "findings": output,
            "category_matched": bool(matching),
        })

    schema = schema_score(schema_outputs)
    properties = property_score(schema_outputs)
    semantic = semantic_score(semantic_results)
    aggregate = (schema + properties + semantic) / 3.0
    result = "PASS" if aggregate >= AGGREGATE_THRESHOLD else "FAIL"

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_score": round(schema, 4),
        "property_score": round(properties, 4),
        "semantic_score": round(semantic, 4),
        "aggregate_score": round(aggregate, 4),
        "threshold": AGGREGATE_THRESHOLD,
        "result": result,
        "case_count": len(dataset),
        "cases": per_case,
    }

    evidence_dir = ROOT / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    report_path = evidence_dir / "evaluation_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Schema score: {schema:.2%}")
    print(f"Property score: {properties:.2%}")
    print(f"Semantic score: {semantic:.2%}")
    print(f"Aggregate score: {aggregate:.2%}")
    print(f"Threshold: {AGGREGATE_THRESHOLD:.2%}")
    print(f"PASS/FAIL: {result}")
    print(f"Report: {report_path}")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
