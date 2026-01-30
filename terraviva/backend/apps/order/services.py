"""
Order services - Business logic layer.

This module contains the business logic for order processing,
separating concerns from views (controllers) and models (entities).
"""

from decimal import Decimal
from typing import Any

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction

from .models import Order, OrderItem


class PaymentError(Exception):
    """Raised when payment processing fails."""

    pass


class PaymentService:
    """
    Service for processing payments via Stripe.

    Encapsulates all Stripe-related logic, making it easier to:
    - Test with mocks
    - Switch payment providers
    - Handle payment errors consistently
    """

    def __init__(self) -> None:
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def charge(self, amount: Decimal, token: str, description: str = "Terra Viva Purchase") -> str:
        """
        Process a payment charge.

        Args:
            amount: Amount in decimal (e.g., 99.99)
            token: Stripe token from frontend
            description: Charge description

        Returns:
            Stripe charge ID

        Raises:
            PaymentError: If payment fails
        """
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),  # Stripe expects cents
                currency="USD",
                description=description,
                source=token,
            )
            return charge.id
        except stripe.error.CardError as e:
            raise PaymentError(f"Card declined: {e.user_message}") from e
        except stripe.error.StripeError as e:
            raise PaymentError(f"Payment failed: {str(e)}") from e


class OrderService:
    """
    Service for order business logic.

    Handles order creation, total calculation, and coordinates
    with PaymentService for checkout flow.
    """

    def __init__(self, payment_service: PaymentService | None = None) -> None:
        self.payment_service = payment_service or PaymentService()

    def calculate_total(self, items: list[dict[str, Any]]) -> Decimal:
        """
        Calculate order total from items.

        Args:
            items: List of dicts with 'quantity' and 'product' keys

        Returns:
            Total amount as Decimal
        """
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
        """
        items_data = validated_data.pop("items")
        stripe_token = validated_data.pop("stripe_token")

        # Calculate total
        paid_amount = self.calculate_total(items_data)

        # Process payment
        self.payment_service.charge(
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
