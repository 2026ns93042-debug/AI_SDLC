from src.rate_limiter import RateLimiter


def test_free_user_is_blocked_after_ten_requests():
    limiter = RateLimiter(clock=lambda: 100.0)
    results = [limiter.check("free-1", "Free") for _ in range(11)]

    assert all(result.allowed for result in results[:10])
    assert results[9].remaining == 0
    assert not results[10].allowed
    assert results[10].remaining == 0


def test_premium_limit():
    limiter = RateLimiter(clock=lambda: 100.0)
    results = [limiter.check("premium-1", "Premium") for _ in range(51)]

    assert sum(result.allowed for result in results) == 50
    assert results[49].remaining == 0
    assert not results[50].allowed


def test_enterprise_limit():
    limiter = RateLimiter(clock=lambda: 100.0)
    results = [limiter.check("enterprise-1", "Enterprise") for _ in range(201)]

    assert sum(result.allowed for result in results) == 200
    assert not results[200].allowed


def test_window_resets_after_expiry():
    now = [100.0]
    limiter = RateLimiter(window_seconds=60, clock=lambda: now[0])

    for _ in range(10):
        assert limiter.check("user", "Free").allowed
    assert not limiter.check("user", "Free").allowed

    now[0] = 160.0
    result = limiter.check("user", "Free")
    assert result.allowed
    assert result.remaining == 9


def test_remaining_quota_is_calculated():
    limiter = RateLimiter(clock=lambda: 100.0)
    assert limiter.check("user", "Premium").remaining == 49
    assert limiter.check("user", "Premium").remaining == 48


def test_reset_method():
    limiter = RateLimiter(clock=lambda: 100.0)
    for _ in range(10):
        limiter.check("user", "Free")
    limiter.reset("user")
    assert limiter.check("user", "Free").allowed


def test_get_remaining_does_not_consume_quota():
    limiter = RateLimiter(clock=lambda: 100.0)
    assert limiter.get_remaining("user", "Free") == 10
    assert limiter.check("user", "Free").remaining == 9
    assert limiter.get_remaining("user", "Free") == 9
