"""In-memory fixed-window rate limiter."""

import threading
import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional

try:
    from .tier_config import TIER_CONFIG, InvalidTierError, validate_tier
except ImportError:
    from tier_config import TIER_CONFIG, InvalidTierError, validate_tier


WINDOW_SECONDS = 60


@dataclass
class LimitResult:
    allowed: bool
    remaining: int
    limit: int
    reset_after: float


@dataclass
class _Window:
    count: int = 0
    window_start: Optional[float] = None


class RateLimiter:
    """Thread-safe fixed-window rate limiter keyed by user identifier."""

    def __init__(
        self,
        window_seconds: float = WINDOW_SECONDS,
        clock: Optional[Callable[[], float]] = None,
    ) -> None:
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        self.window_seconds = float(window_seconds)
        self._clock = clock or time.time
        self._windows: Dict[str, _Window] = {}
        self._lock = threading.RLock()

    def check(self, user_id: str, tier: str) -> LimitResult:
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id must be a non-empty string")
        tier = validate_tier(tier)
        limit = TIER_CONFIG[tier].limit
        now = float(self._clock())

        with self._lock:
            window = self._windows.get(user_id)
            if window is None or window.window_start is None:
                window = _Window(window_start=now)
                self._windows[user_id] = window
            elif now - window.window_start >= self.window_seconds:
                window.count = 0
                window.window_start = now

            elapsed = max(0.0, now - window.window_start)
            reset_after = max(0.0, self.window_seconds - elapsed)

            if window.count >= limit:
                return LimitResult(False, 0, limit, reset_after)

            window.count += 1
            return LimitResult(True, max(0, limit - window.count), limit, reset_after)

    def is_allowed(self, user_id: str, tier: str) -> bool:
        return self.check(user_id, tier).allowed

    def get_remaining(self, user_id: str, tier: str) -> int:
        tier = validate_tier(tier)
        limit = TIER_CONFIG[tier].limit
        now = float(self._clock())
        with self._lock:
            window = self._windows.get(user_id)
            if window is None or window.window_start is None:
                return limit
            if now - window.window_start >= self.window_seconds:
                return limit
            return max(0, limit - window.count)

    def allow_request(self, user_id: str, tier: str) -> bool:
        return self.is_allowed(user_id, tier)

    def get_remaining_quota(self, user_id: str, tier: str) -> int:
        return self.get_remaining(user_id, tier)

    def reset(self, user_id: Optional[str] = None) -> None:
        with self._lock:
            if user_id is None:
                self._windows.clear()
            else:
                self._windows.pop(user_id, None)


# Backwards-friendly aliases for simple integrations.
TierLimitExceeded = InvalidTierError


def check_request(
    user_id: str,
    tier: str,
    limiter: Optional[RateLimiter] = None,
) -> LimitResult:
    return (limiter or RateLimiter()).check(user_id, tier)
