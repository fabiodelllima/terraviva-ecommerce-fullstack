"""
Order services - Application layer.

Business logic for order processing, coordinating between
domain entities, validators, and infrastructure gateways.
"""

from decimal import Decimal
from typing import Any

from django.contrib.auth.models import User
from django.db import transaction

from .gateways import StripeGateway
from .models import Order, OrderItem
from .validators import validate_order_items


class OrderService:
    """
    Service for order business logic.

    Handles order creation, total calculation, and coordinates
    with payment gateway for checkout flow.
    """

    def __init__(self, payment_gateway: StripeGateway | None = None) -> None:
        self.payment_gateway = payment_gateway or StripeGateway()

    def calculate_total(self, items: list[dict[str, Any]]) -> Decimal:
        """
        Calculate order total from items.

        Args:
            items: List of dicts with 'quantity' and 'product' keys

        Returns:
            Total amount as Decimal

        Raises:
            InvalidOrderError: If items are invalid
        """
        validate_order_items(items)

        total = Decimal("0.00")
        for item in items:
            quantity = item.get("quantity", 1)
            product = item.get("product")
            if product:
                total += Decimal(str(quantity)) * product.price
        return total

    @transaction.atomic()
    def create_order(
        self,
        user: User,
        order_data: dict[str, Any],
        items_data: list[dict[str, Any]],
    ) -> Order:
        """
        Create an order with its items.

        Args:
            user: The user placing the order
            order_data: Order fields (address, phone, etc.)
            items_data: List of order items

        Returns:
            Created Order instance
        """
        order = Order.objects.create(user=user, **order_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def process_checkout(
        self,
        user: User,
        validated_data: dict[str, Any],
    ) -> Order:
        """
        Process complete checkout flow.

        1. Calculate total
        2. Process payment
        3. Create order

        Args:
            user: Authenticated user
            validated_data: Validated order data from serializer

        Returns:
            Created Order instance

        Raises:
            PaymentError: If payment fails
            InvalidOrderError: If order data is invalid
        """
        items_data = validated_data.pop("items")
        stripe_token = validated_data.pop("stripe_token")

        # Calculate total
        paid_amount = self.calculate_total(items_data)

        # Process payment via gateway
        self.payment_gateway.charge(
            amount=paid_amount,
            token=stripe_token,
            description=f"Terra Viva - Order for {user.email}",
        )

        # Create order
        order = self.create_order(
            user=user,
            order_data={**validated_data, "stripe_token": stripe_token, "paid_amount": paid_amount},
            items_data=items_data,
        )

        return order
