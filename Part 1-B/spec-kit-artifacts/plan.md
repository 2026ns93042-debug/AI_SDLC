# Implementation Plan

1. Implement `review_source` and `review_file` in `src/code_review_agent.py`.
2. Enforce the output contract with `harness/schema_validator.py`.
3. Verify structural invariants with `harness/property_validator.py`.
4. Compare reviewed findings to expected categories and locations in
   `harness/semantic_evaluator.py`.
5. Provide 18 evaluation cases covering categories and edge cases.
6. Execute the runner, inspect evidence, and fix the agent or expected cases
   if aggregate acceptance is below 80%.
7. Verify behavior with focused pytest tests.
