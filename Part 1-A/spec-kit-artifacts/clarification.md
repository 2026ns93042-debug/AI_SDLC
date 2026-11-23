# Clarification

- A fixed-window model is used. Window boundaries are one 60-second interval from the user's first request.
- One counter is maintained per user ID and tier configuration is validated separately.
- Blocked requests do not increase the counter or consume additional quota.
- Invalid tier names are rejected as `InvalidTierError`.
- The in-memory implementation is resettable and is intended for one process.
