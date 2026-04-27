"""Tests for product app."""

from io import BytesIO
from unittest.mock import MagicMock, PropertyMock

import pytest
from django.core.files import File
from PIL import Image

from apps.product.services import ImageService

# =============================================================================
# Endpoint smoke tests
# =============================================================================


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


# =============================================================================
# ImageService.make_thumbnail
# =============================================================================


def _make_test_image(
    size: tuple[int, int] = (800, 600),
    mode: str = "RGB",
    fmt: str = "JPEG",
    name: str = "test.jpg",
) -> File:
    """Create an in-memory image wrapped as Django File for testing."""
    img = Image.new(mode, size, color=(255, 0, 0))
    buffer = BytesIO()
    img.save(buffer, format=fmt)
    buffer.seek(0)
    return File(buffer, name=name)


class TestMakeThumbnail:
    """Tests for ImageService.make_thumbnail."""

    def test_returns_django_file(self):
        """Thumbnail output must be a Django File instance."""
        source = _make_test_image()
        result = ImageService.make_thumbnail(source)
        assert isinstance(result, File)

    def test_preserves_filename(self):
        """Thumbnail filename must match source basename."""
        source = _make_test_image(name="product-photo.jpg")
        result = ImageService.make_thumbnail(source)
        assert result.name == "product-photo.jpg"

    def test_default_size_fits_within_300x200(self):
        """Default thumbnail must fit within 300x200 bounds."""
        source = _make_test_image(size=(800, 600))
        result = ImageService.make_thumbnail(source)
        with Image.open(result) as thumb:
            width, height = thumb.size
        assert width <= 300
        assert height <= 200

    def test_custom_size_is_respected(self):
        """Custom size argument must override default bounds."""
        source = _make_test_image(size=(800, 600))
        result = ImageService.make_thumbnail(source, size=(100, 100))
        with Image.open(result) as thumb:
            width, height = thumb.size
        assert width <= 100
        assert height <= 100

    def test_output_is_jpeg(self):
        """Thumbnail must be saved as JPEG regardless of input format."""
        source = _make_test_image(fmt="PNG", name="image.png")
        result = ImageService.make_thumbnail(source)
        with Image.open(result) as thumb:
            assert thumb.format == "JPEG"

    def test_converts_rgba_to_rgb(self):
        """RGBA source must be converted to RGB for JPEG compatibility."""
        source = _make_test_image(mode="RGBA", fmt="PNG", name="alpha.png")
        result = ImageService.make_thumbnail(source)
        with Image.open(result) as thumb:
            assert thumb.mode == "RGB"

    def test_quality_argument_affects_output_size(self):
        """Lower quality must produce a smaller file than higher quality."""
        source_high = _make_test_image()
        source_low = _make_test_image()
        high = ImageService.make_thumbnail(source_high, quality=95)
        low = ImageService.make_thumbnail(source_low, quality=20)
        high.seek(0)
        low.seek(0)
        assert len(low.read()) < len(high.read())


# =============================================================================
# ImageService.get_safe_url
# =============================================================================


class TestGetSafeUrl:
    """Tests for ImageService.get_safe_url."""

    def test_none_field_returns_empty_string(self):
        """None input must return empty string, not raise."""
        assert ImageService.get_safe_url(None) == ""

    def test_falsy_field_returns_empty_string(self):
        """Falsy field (e.g., empty ImageFieldFile) must return empty string."""
        falsy_field = MagicMock()
        falsy_field.__bool__ = MagicMock(return_value=False)
        assert ImageService.get_safe_url(falsy_field) == ""

    def test_field_without_url_attribute_returns_empty_string(self):
        """Field missing .url attribute must return empty string."""
        field = MagicMock(spec=[])  # spec=[] removes all auto-generated attrs
        assert ImageService.get_safe_url(field) == ""

    def test_field_with_url_returns_url_string(self):
        """Valid field must return its .url as string."""
        field = MagicMock()
        field.url = "https://example.com/media/image.jpg"
        assert ImageService.get_safe_url(field) == "https://example.com/media/image.jpg"

    def test_field_url_access_raising_returns_empty_string(self):
        """Exception on .url access must be caught and return empty string."""
        field = MagicMock()
        type(field).url = PropertyMock(side_effect=ValueError("no file"))
        assert ImageService.get_safe_url(field) == ""

    def test_field_with_none_url_returns_empty_string(self):
        """Field where .url is None must return empty string."""
        field = MagicMock()
        field.url = None
        assert ImageService.get_safe_url(field) == ""
