# Implementation Plan

1. Define immutable tier metadata and tier validation.
2. Implement a thread-safe fixed-window limiter with an injectable clock.
3. Add a framework-independent API adapter with stable result dictionaries.
4. Create unit tests for every tier, reset behavior, remaining quota, and errors.
5. Add lint, security, pytest, and all-in-one harnesses.
6. Run pytest, coverage, and the harness, then record evidence.
