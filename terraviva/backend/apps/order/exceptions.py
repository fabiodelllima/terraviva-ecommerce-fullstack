"""
Order domain exceptions.

Centralized exceptions for the order module.
"""


class OrderException(Exception):
    """Base exception for order domain."""

    pass


class PaymentError(OrderException):
    """Raised when payment processing fails."""

    pass


class InvalidOrderError(OrderException):
    """Raised when order data is invalid."""

    pass
