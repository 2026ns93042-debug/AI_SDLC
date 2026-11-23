# Constitution

- Implement deterministic, correct per-tier request limiting.
- Use a clear fixed-window of 60 seconds.
- Validate every tier before processing a request.
- Preserve thread safety for shared limiter state.
- Keep the implementation dependency-free except for the test tooling.
- Make every behavior observable through tests and harness scripts.
