Part 1A - Tiered Rate Limiter Microservice
Objective
Build a deterministic Tiered Rate Limiter Microservice.

Supported tiers:

Free

10 requests per minute
Premium

50 requests per minute
Enterprise

200 requests per minute
Features
Request counting
Rate limit enforcement
Remaining quota tracking
Automatic window reset
Tier validation
Acceptance Criteria
Free users are blocked after 10 requests.
Premium users are blocked after 50 requests.
Enterprise users are blocked after 200 requests.
Limits reset after window expiry.
Invalid tier returns an error.
Remaining quota is calculated correctly.
Required Structure
Part-1A/ ├── spec-kit-artifacts/ │ ├── constitution.md │ ├── specification.md │ ├── clarification.md │ ├── plan.md │ └── tasks.md │ ├── src/ ├── tests/ ├── harness/ ├── evidence/ │ ├── README.md └── requirements.txt

Required Source Files
src/rate_limiter.py src/tier_config.py src/api.py

Required Tests
tests/test_rate_limiter.py tests/test_tiers.py tests/test_api.py

Harness Files
harness/lint_check.py harness/security_check.py harness/run_tests.py harness/run_all.py

Required Execution Flow
pytest python harness/run_all.py coverage run -m pytest coverage report

Generate a fully working implementation and test suite.