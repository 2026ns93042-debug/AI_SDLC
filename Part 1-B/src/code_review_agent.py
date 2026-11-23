"""Deterministic AI-assisted code review agent."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterable


VALID_CATEGORIES = {"Bug", "Security", "Performance", "Style", "Maintainability"}
VALID_SEVERITIES = {"Low", "Medium", "High"}


def _finding(category: str, severity: str, line: int, finding: str, suggestion: str) -> dict:
    return {
        "category": category,
        "severity": severity,
        "line": line,
        "finding": finding,
        "suggestion": suggestion,
    }


def review_source(source: str) -> list[dict]:
    """Review Python source and return structured findings."""
    findings: list[dict] = []
    lines = source.splitlines()
    none_names: set[str] = set()

    for index, text in enumerate(lines, start=1):
        stripped = text.strip()
        if not stripped or stripped.startswith("#"):
            continue

        lower = stripped.lower()

        if re.search(r"\b(eval|exec)\s*\(", lower):
            findings.append(_finding(
                "Security", "High", index,
                "Use of eval or exec can execute arbitrary code",
                "Use explicit parsing or a safe allowlisted implementation",
            ))

        if "shell=true" in lower:
            findings.append(_finding(
                "Security", "High", index,
                "Subprocess shell execution may enable command injection",
                "Avoid shell=True and pass an argument list with strict validation",
            ))

        secret_match = re.search(r"\b(password|passwd|secret|api[_-]?key)\b\s*=", lower)
        if secret_match:
            findings.append(_finding(
                "Security", "High", index,
                "A credential appears to be stored directly in source",
                "Load the credential from environment variables or a secret manager",
            ))

        if re.search(r"\b(pickle\.loads?|yaml\.load)\s*\(", lower):
            findings.append(_finding(
                "Security", "High", index,
                "Deserializing untrusted data can execute attacker-controlled code",
                "Use a safe format or validate and deserialize only trusted input",
            ))

        if re.search(r"(^|[^.\w])hashlib\.md5\s*\(", lower) or re.search(r"(^|[^.\w])hashlib\.sha1\s*\(", lower):
            findings.append(_finding(
                "Security", "Medium", index,
                "Weak cryptographic hash algorithm may be unsuitable for security",
                "Use SHA-256 or a stronger approved hash for security-sensitive operations",
            ))

        if re.search(r"\bexecute\s*\(\s*(?:f[\"']|[\"'][^\"']*[\"']\s*\+)", lower):
            findings.append(_finding(
                "Security", "High", index,
                "SQL query construction may allow SQL injection",
                "Use a parameterized query and pass values separately",
            ))

        if re.search(r"/\s*0(?:\.0)?(?:\b|$)", stripped):
            findings.append(_finding(
                "Bug", "High", index,
                "Division by zero is possible",
                "Validate that the denominator is non-zero before division",
            ))

        divide_match = re.search(r"\b(\w+)\s*/\s*(\w+)", stripped)
        if divide_match and divide_match.group(2).lower() in {"denominator", "divisor"}:
            findings.append(_finding(
                "Bug", "High", index,
                "Division uses a potentially zero denominator",
                "Check the denominator value before performing division",
            ))

        if re.search(r"\bNone\b.*\.", stripped) or re.search(r"\.\w+\s*\(", stripped):
            if re.search(r"\bNone\b", stripped):
                findings.append(_finding(
                    "Bug", "High", index,
                    "Potential null value dereference",
                    "Check for None before accessing attributes or calling methods",
                ))
        none_assignment = re.match(r"\b([A-Za-z_]\w*)\s*=\s*None\b", stripped)
        if none_assignment:
            none_names.add(none_assignment.group(1))
        dereference_match = re.search(r"\b([A-Za-z_]\w*)\s*\.", stripped)
        if dereference_match and dereference_match.group(1) in none_names:
            findings.append(_finding(
                "Bug", "High", index,
                "Potential null value dereference",
                "Check for None before accessing attributes or calling methods",
            ))

        if re.search(r"==\s*(True|False)\b|!=\s*(True|False)\b", stripped):
            findings.append(_finding(
                "Style", "Low", index,
                "Boolean comparison is unnecessarily explicit",
                "Use the boolean value directly or use its negation",
            ))

        if re.search(r"\bexcept\s*(Exception)?\s*:", stripped):
            if "except:" in stripped or "except Exception:" in stripped:
                findings.append(_finding(
                    "Maintainability", "Medium", index,
                    "Broad exception handling hides failures and reduces diagnosability",
                    "Catch specific exception types and handle or re-raise them appropriately",
                ))

        if re.search(r"\bpass\s*(?:#.*)?$", stripped):
            findings.append(_finding(
                "Maintainability", "Medium", index,
                "Empty exception or control block is likely incomplete",
                "Add explicit error handling or an explanatory comment",
            ))

        if re.search(r"\b(?:s|text|result|output)\s*\+=" , lower):
            findings.append(_finding(
                "Performance", "Medium", index,
                "Repeated string concatenation can create avoidable allocations",
                "Collect strings in a list and join them once",
            ))

        if re.search(r"\bappend\s*\(", lower):
            findings.append(_finding(
                "Performance", "Low", index,
                "Repeated collection updates may be costly in a tight loop",
                "Preallocate or batch collection work where it preserves behavior",
            ))

        if re.search(r"\blen\s*\(\s*\w+\s*\)\s*[><=!]", lower):
            findings.append(_finding(
                "Performance", "Low", index,
                "Collection length appears to be recomputed in a loop",
                "Cache the length outside the loop when it does not change",
            ))

    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and len(node.args.args) > 5:
                findings.append(_finding(
                    "Maintainability", "Medium", node.lineno,
                    "Function has too many parameters",
                    "Group related parameters in an object or reduce the public interface",
                ))
    except SyntaxError:
        pass

    unique = []
    seen = set()
    for item in findings:
        key = (item["category"], item["line"], item["finding"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def review_file(path: str | Path) -> list[dict]:
    """Read and review a Python source file."""
    return review_source(Path(path).read_text(encoding="utf-8"))
