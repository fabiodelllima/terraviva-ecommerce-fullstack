"""Tests for product app."""

import pytest


@pytest.mark.django_db
class TestProductEndpoints:
    """Basic smoke tests for product endpoints."""

    def test_latest_products_endpoint_exists(self, client):
        """Test that latest products endpoint returns 200."""
        response = client.get("/api/v1/latest-products/")
        assert response.status_code == 200

    def test_products_search_endpoint_exists(self, client):
        """Test that search endpoint returns 200."""
        response = client.post("/api/v1/products/search/", {"query": "test"})
        assert response.status_code == 200
