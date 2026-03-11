"""
Order validators - Defensive programming.

Guard clauses and validation functions for fail-fast behavior.
"""

from decimal import Decimal
from typing import Any

from .exceptions import InvalidOrderError


def validate_amount(amount: Decimal | None) -> None:
    """
    Validate payment amount.

    Args:
        amount: Payment amount to validate

    Raises:
        InvalidOrderError: If amount is invalid
    """
    if amount is None:
        raise InvalidOrderError("Amount is required")
    if not isinstance(amount, Decimal):
        raise InvalidOrderError("Amount must be a Decimal")
    if amount <= 0:
        raise InvalidOrderError("Amount must be positive")


def validate_payment_token(token: str | None) -> None:
    """
    Validate payment token.

    Args:
        token: Stripe token to validate

    Raises:
        InvalidOrderError: If token is invalid
    """
    if not token:
        raise InvalidOrderError("Payment token is required")
    if not isinstance(token, str):
        raise InvalidOrderError("Payment token must be a string")
    if not token.strip():
        raise InvalidOrderError("Payment token cannot be empty")


def validate_order_items(items: list[dict[str, Any]] | None) -> None:
    """
    Validate order items.

    Args:
        items: List of order items to validate

    Raises:
        InvalidOrderError: If items are invalid
    """
    if not items:
        raise InvalidOrderError("Order must have at least one item")

    for i, item in enumerate(items):
        if not item.get("product"):
            raise InvalidOrderError(f"Item {i + 1} must have a product")
        quantity = item.get("quantity", 1)
        if quantity < 1:
            raise InvalidOrderError(f"Item {i + 1} quantity must be at least 1")
