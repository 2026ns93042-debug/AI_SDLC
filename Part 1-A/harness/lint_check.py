"""Basic source lint harness."""

import ast
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def run() -> bool:
    failed = False
    for directory in ("src", "tests", "harness"):
        for path in (ROOT / directory).glob("*.py"):
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                print("SYNTAX ERROR:", exc)
                failed = True
    print("Lint check:", "FAILED" if failed else "PASSED")
    return not failed


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
