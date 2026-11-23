from src.api import RateLimitAPI
from src.rate_limiter import RateLimiter


def test_api_allows_requests_and_reports_remaining():
    api = RateLimitAPI(RateLimiter(clock=lambda: 100.0))
    response = api.process_request("api-user", "Free")

    assert response["status"] == 200
    assert response["allowed"] is True
    assert response["remaining"] == 9


def test_api_returns_429_after_limit():
    api = RateLimitAPI(RateLimiter(clock=lambda: 100.0))
    for _ in range(10):
        api.process_request("api-user", "Free")

    response = api.process_request("api-user", "Free")
    assert response["status"] == 429
    assert response["allowed"] is False
    assert response["remaining"] == 0


def test_api_invalid_tier_error():
    api = RateLimitAPI()
    response = api.process_request("api-user", "Unsupported")

    assert response["status"] == 400
    assert "error" in response
