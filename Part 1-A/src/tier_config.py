"""Tier definitions and tier validation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Tier:
    name: str
    limit: int


TIER_CONFIG = {
    "Free": Tier("Free", 10),
    "Premium": Tier("Premium", 50),
    "Enterprise": Tier("Enterprise", 200),
}

# Common aliases make the module convenient for callers and test suites.
TIER_LIMITS = {name: tier.limit for name, tier in TIER_CONFIG.items()}


class InvalidTierError(ValueError):
    """Raised when a tier name is not supported."""


def validate_tier(tier: str) -> str:
    """Validate and normalize a tier name."""
    if not isinstance(tier, str):
        raise InvalidTierError("Invalid tier")
    normalized = tier.strip().lower()
    aliases = {name.lower(): name for name in TIER_CONFIG}
    if normalized not in aliases:
        raise InvalidTierError("Invalid tier")
    return aliases[normalized]


def get_tier_limit(tier: str) -> int:
    """Return the requests-per-minute limit for a tier."""
    return TIER_CONFIG[validate_tier(tier)].limit
