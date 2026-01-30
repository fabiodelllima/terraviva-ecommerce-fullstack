"""Tests for order app."""

import pytest


@pytest.mark.django_db
class TestOrderEndpoints:
    """Basic smoke tests for order endpoints."""

    def test_checkout_requires_auth(self, client):
        """Test that checkout endpoint requires authentication."""
        response = client.post("/api/v1/checkout/")
        assert response.status_code in [401, 403]

    def test_orders_requires_auth(self, client):
        """Test that orders endpoint requires authentication."""
        response = client.get("/api/v1/orders/")
        assert response.status_code in [401, 403]
