# Specification

## Product

A deterministic tiered rate limiter microservice core that tracks request counts for each user.

## Supported tiers

| Tier | Requests per minute |
|---|---:|
| Free | 10 |
| Premium | 50 |
| Enterprise | 200 |

## Behavior

- Count successful and blocked requests within a 60-second fixed window.
- Reject further requests once the tier limit is reached.
- Return the remaining quota, limit, and reset delay.
- Reset the window exactly after window expiry.
- Return an error for invalid tiers.

## API behavior

- Allowed requests use HTTP status 200.
- Rejected requests use HTTP status 429.
- Invalid input or tier use HTTP status 400.
