# Tiered Rate Limiter Microservice

A deterministic fixed-window rate limiter for Free, Premium, and Enterprise tiers.

## Structure

- `src/rate_limiter.py` - thread-safe in-memory limiter
- `src/tier_config.py` - tier definitions and validation
- `src/api.py` - framework-independent API adapter
- `tests/` - pytest unit tests
- `harness/` - lint, security, tests, and full-run scripts
- `spec-kit-artifacts/` - specification artifacts
- `evidence/` - generated validation records

## Tier limits

| Tier | Limit |
|---|---:|
| Free | 10 requests/minute |
| Premium | 50 requests/minute |
| Enterprise | 200 requests/minute |

## Run

```powershell
pytest
python harness/run_all.py
coverage run -m pytest
coverage report
```

## Usage

```python
from src.api import RateLimitAPI

api = RateLimitAPI()
response = api.process_request("customer-123", "Premium")
print(response)
```
