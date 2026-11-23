"""Small dependency-free security sanity checks."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def run() -> bool:
    forbidden = ("eval(", "exec(", "subprocess", "pickle.loads")
    failures = []
    for path in (ROOT / "src").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            if pattern in text:
                failures.append(f"{path.name}: forbidden pattern {pattern}")
    print("Security check:", "FAILED" if failures else "PASSED")
    for failure in failures:
        print(failure)
    return not failures


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
