"""Small framework-independent HTTP-style API for the rate limiter."""

from typing import Dict, Optional

try:
    from .rate_limiter import RateLimiter
    from .tier_config import InvalidTierError
except ImportError:
    from rate_limiter import RateLimiter
    from tier_config import InvalidTierError


class RateLimitAPI:
    def __init__(self, limiter: Optional[RateLimiter] = None) -> None:
        self.limiter = limiter or RateLimiter()

    def process_request(self, user_id: str, tier: str) -> Dict[str, object]:
        try:
            result = self.limiter.check(user_id, tier)
        except InvalidTierError as exc:
            return {"status": 400, "error": str(exc)}
        except ValueError as exc:
            return {"status": 400, "error": str(exc)}

        if result.allowed:
            return {
                "status": 200,
                "allowed": True,
                "remaining": result.remaining,
                "limit": result.limit,
                "reset_after": result.reset_after,
            }
        return {
            "status": 429,
            "allowed": False,
            "remaining": 0,
            "limit": result.limit,
            "reset_after": result.reset_after,
        }

    def handle_request(self, user_id: str, tier: str) -> Dict[str, object]:
        return self.process_request(user_id, tier)


def process_request(
    user_id: str,
    tier: str,
    limiter: Optional[RateLimiter] = None,
) -> Dict[str, object]:
    return RateLimitAPI(limiter).process_request(user_id, tier)
