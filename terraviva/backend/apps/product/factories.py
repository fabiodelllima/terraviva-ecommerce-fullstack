"""
Test factories for product models.

Provides factory_boy factories for creating Category and Product
instances in tests, avoiding boilerplate model setup.
"""

from decimal import Decimal

import factory
from factory.django import DjangoModelFactory

from apps.product.models import Category, Product


class CategoryFactory(DjangoModelFactory):
    """Factory for Category model."""

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")


class ProductFactory(DjangoModelFactory):
    """Factory for Product model."""

    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.Sequence(lambda n: f"Product {n}")
    slug = factory.Sequence(lambda n: f"product-{n}")
    description = factory.Faker("paragraph", nb_sentences=3)
    price = factory.LazyFunction(lambda: Decimal("99.90"))
