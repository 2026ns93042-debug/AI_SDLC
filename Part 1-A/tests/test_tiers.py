import pytest

from src.tier_config import (
    TIER_LIMITS,
    InvalidTierError,
    get_tier_limit,
    validate_tier,
)


def test_supported_tier_limits():
    assert TIER_LIMITS == {"Free": 10, "Premium": 50, "Enterprise": 200}


@pytest.mark.parametrize(
    ("tier", "limit"),
    [("Free", 10), ("Premium", 50), ("Enterprise", 200)],
)
def test_get_tier_limit(tier, limit):
    assert get_tier_limit(tier) == limit


def test_tier_validation_is_case_insensitive():
    assert validate_tier("premium") == "Premium"


@pytest.mark.parametrize("tier", ["", "Basic", "unknown", None])
def test_invalid_tier(tier):
    with pytest.raises(InvalidTierError):
        validate_tier(tier)
