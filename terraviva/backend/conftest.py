"""Pytest configuration for Terra Viva Backend."""

import os

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings_test"
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("DEBUG", "True")

import django
import pytest

django.setup()


@pytest.fixture
def api_client():
    """Return DRF APIClient instance."""
    from rest_framework.test import APIClient

    return APIClient()
