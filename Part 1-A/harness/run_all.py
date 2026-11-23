"""Run tests, lint, and security checks."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_command(args):
    return subprocess.call([sys.executable, *args], cwd=ROOT)


def main() -> int:
    print("== pytest ==")
    if run_command(["-m", "pytest", "-q"]) != 0:
        return 1
    print("== lint ==")
    if run_command(["harness/lint_check.py"]) != 0:
        return 1
    print("== security ==")
    if run_command(["harness/security_check.py"]) != 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
