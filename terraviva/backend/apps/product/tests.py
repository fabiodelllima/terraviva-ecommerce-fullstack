"""Tests for product app."""

from io import BytesIO
from unittest.mock import MagicMock, PropertyMock

import pytest
from django.core.files import File
from PIL import Image

from apps.product.factories import CategoryFactory, ProductFactory
from apps.product.selectors import (
    get_category_by_slug,
    get_latest_products,
    get_product_by_slugs,
    search_products,
)
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
        field = MagicMock(spec=[])
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


# =============================================================================
# Selectors
# =============================================================================


@pytest.mark.django_db
class TestGetLatestProducts:
    """Tests for get_latest_products selector."""

    def test_returns_empty_queryset_when_no_products(self):
        """Empty database must return empty queryset."""
        result = get_latest_products()
        assert result.count() == 0

    def test_returns_products_ordered_by_date_added_desc(self):
        """Most recently added products must come first."""
        first = ProductFactory()
        second = ProductFactory()
        third = ProductFactory()
        result = list(get_latest_products())
        assert result[0] == third
        assert result[1] == second
        assert result[2] == first

    def test_default_limit_is_8(self):
        """Default limit must cap result at 8 products."""
        ProductFactory.create_batch(10)
        result = get_latest_products()
        assert result.count() == 8

    def test_custom_limit_is_respected(self):
        """Custom limit argument must override default."""
        ProductFactory.create_batch(5)
        result = get_latest_products(limit=3)
        assert result.count() == 3

    def test_limit_larger_than_total_returns_all(self):
        """Limit higher than available products must return all of them."""
        ProductFactory.create_batch(2)
        result = get_latest_products(limit=10)
        assert result.count() == 2


@pytest.mark.django_db
class TestGetProductBySlugs:
    """Tests for get_product_by_slugs selector."""

    def test_returns_product_when_both_slugs_match(self):
        """Matching category and product slugs must return product."""
        category = CategoryFactory(slug="electronics")
        product = ProductFactory(category=category, slug="laptop")
        result = get_product_by_slugs("electronics", "laptop")
        assert result == product

    def test_returns_none_when_product_slug_not_found(self):
        """Unknown product slug must return None instead of raising."""
        category = CategoryFactory(slug="electronics")
        ProductFactory(category=category, slug="laptop")
        result = get_product_by_slugs("electronics", "phone")
        assert result is None

    def test_returns_none_when_category_slug_not_found(self):
        """Unknown category slug must return None instead of raising."""
        category = CategoryFactory(slug="electronics")
        ProductFactory(category=category, slug="laptop")
        result = get_product_by_slugs("clothing", "laptop")
        assert result is None

    def test_returns_none_when_product_belongs_to_different_category(self):
        """Product slug exists but in a different category must return None."""
        cat_a = CategoryFactory(slug="electronics")
        # Second category exists in DB but product is not associated with it.
        CategoryFactory(slug="clothing")
        ProductFactory(category=cat_a, slug="shared-slug")
        result = get_product_by_slugs("clothing", "shared-slug")
        assert result is None


@pytest.mark.django_db
class TestGetCategoryBySlug:
    """Tests for get_category_by_slug selector."""

    def test_returns_category_when_slug_matches(self):
        """Existing slug must return the category instance."""
        category = CategoryFactory(slug="electronics")
        result = get_category_by_slug("electronics")
        assert result == category

    def test_returns_none_when_slug_not_found(self):
        """Unknown slug must return None instead of raising."""
        CategoryFactory(slug="electronics")
        result = get_category_by_slug("nonexistent")
        assert result is None

    def test_returns_none_for_empty_string(self):
        """Empty slug must return None gracefully."""
        result = get_category_by_slug("")
        assert result is None


@pytest.mark.django_db
class TestSearchProducts:
    """Tests for search_products selector."""

    def test_empty_query_returns_empty_queryset(self):
        """Empty query string must return empty queryset without DB hit."""
        ProductFactory.create_batch(3)
        result = search_products("")
        assert result.count() == 0

    def test_finds_product_by_name(self):
        """Query matching product name must return that product."""
        target = ProductFactory(name="Wireless Keyboard")
        ProductFactory(name="USB Cable")
        result = search_products("keyboard")
        assert list(result) == [target]

    def test_finds_product_by_description(self):
        """Query matching product description must return that product."""
        target = ProductFactory(
            name="Item A",
            description="Premium ergonomic design for daily use.",
        )
        ProductFactory(name="Item B", description="Standard cable.")
        result = search_products("ergonomic")
        assert list(result) == [target]

    def test_search_is_case_insensitive(self):
        """Search must match regardless of case."""
        target = ProductFactory(name="Wireless Keyboard")
        result = search_products("KEYBOARD")
        assert list(result) == [target]

    def test_partial_match_in_name(self):
        """Substring of name must match (icontains semantics)."""
        target = ProductFactory(name="Mechanical Keyboard Pro")
        result = search_products("Mechanical")
        assert list(result) == [target]

    def test_no_match_returns_empty(self):
        """Query with no matches must return empty queryset."""
        ProductFactory(name="Wireless Keyboard")
        result = search_products("xyzabc")
        assert result.count() == 0

    def test_matches_multiple_products(self):
        """Query matching multiple products must return all of them."""
        a = ProductFactory(name="Keyboard A")
        b = ProductFactory(name="Keyboard B")
        ProductFactory(name="Mouse")
        result = search_products("keyboard")
        assert set(result) == {a, b}
