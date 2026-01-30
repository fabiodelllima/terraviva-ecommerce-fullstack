"""
Product views - Controller layer.

Thin controllers that delegate queries to selectors.
"""

from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from . import selectors
from .serializers import CategorySerializer, ProductSerializer


class LatestProductsList(APIView):
    """List latest products."""

    def get(self, request, format=None):
        products = selectors.get_latest_products(limit=8)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    """Get product details by category and product slugs."""

    def get(self, request, category_slug, product_slug, format=None):
        product = selectors.get_product_by_slugs(category_slug, product_slug)
        if not product:
            raise Http404
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetail(APIView):
    """Get category details with products."""

    def get(self, request, category_slug, format=None):
        category = selectors.get_category_by_slug(category_slug)
        if not category:
            raise Http404
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(["POST"])
def search(request):
    """Search products by name or description."""
    query = request.data.get("query", "")
    products = selectors.search_products(query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
