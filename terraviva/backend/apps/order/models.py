"""
Order models - Entity layer.

Models are kept thin, delegating business logic to services.
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

from apps.product.models import Product


class Order(models.Model):
    """Order entity representing a customer purchase."""

    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    stripe_token = models.CharField(max_length=100)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order #{self.id} - {self.full_name}"

    @property
    def full_name(self) -> str:
        """Get customer full name."""
        return f"{self.first_name} {self.last_name}"


class OrderItem(models.Model):
    """Order item representing a product in an order."""

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name}"

    @property
    def total(self) -> Decimal:
        """Calculate item total."""
        return Decimal(str(self.price)) * self.quantity
