"""
Product selectors - Query layer.

This module contains query logic separated from views,
making queries reusable and testable.
"""

from django.db.models import Q, QuerySet

from .models import Category, Product


def get_latest_products(limit: int = 8) -> QuerySet[Product]:
    """
    Get the most recently added products.

    Args:
        limit: Maximum number of products to return

    Returns:
        QuerySet of latest products
    """
    return Product.objects.all()[:limit]


def get_product_by_slugs(category_slug: str, product_slug: str) -> Product | None:
    """
    Get a product by category and product slugs.

    Args:
        category_slug: Category slug
        product_slug: Product slug

    Returns:
        Product instance or None if not found
    """
    try:
        return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
    except Product.DoesNotExist:
        return None


def get_category_by_slug(slug: str) -> Category | None:
    """
    Get a category by slug.

    Args:
        slug: Category slug

    Returns:
        Category instance or None if not found
    """
    try:
        return Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return None


def search_products(query: str) -> QuerySet[Product]:
    """
    Search products by name or description.

    Args:
        query: Search term

    Returns:
        QuerySet of matching products
    """
    if not query:
        return Product.objects.none()

    return Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
