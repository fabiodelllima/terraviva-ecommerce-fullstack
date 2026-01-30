"""Pytest configuration for Terra Viva Backend."""

import os

import django
import pytest


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()
