"""Tests for order app."""

from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from apps.order.exceptions import InvalidOrderError, PaymentError
from apps.order.gateways import StripeGateway
from apps.order.services import OrderService
from apps.order.validators import (
    validate_amount,
    validate_order_items,
    validate_payment_token,
)

# =============================================================================
# Validator Tests
# =============================================================================


class TestValidateAmount:
    """Tests for validate_amount function."""

    def test_valid_amount(self):
        """Valid decimal amount should not raise."""
        validate_amount(Decimal("10.00"))
        validate_amount(Decimal("0.01"))
        validate_amount(Decimal("9999.99"))

    def test_none_amount_raises(self):
        """None amount should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Amount is required"):
            validate_amount(None)

    def test_non_decimal_raises(self):
        """Non-Decimal amount should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Amount must be a Decimal"):
            validate_amount(10.00)  # type: ignore
        with pytest.raises(InvalidOrderError, match="Amount must be a Decimal"):
            validate_amount("10.00")  # type: ignore

    def test_zero_amount_raises(self):
        """Zero amount should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Amount must be positive"):
            validate_amount(Decimal("0"))

    def test_negative_amount_raises(self):
        """Negative amount should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Amount must be positive"):
            validate_amount(Decimal("-10.00"))


class TestValidatePaymentToken:
    """Tests for validate_payment_token function."""

    def test_valid_token(self):
        """Valid token should not raise."""
        validate_payment_token("tok_visa")
        validate_payment_token("tok_mastercard")

    def test_none_token_raises(self):
        """None token should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Payment token is required"):
            validate_payment_token(None)

    def test_empty_string_raises(self):
        """Empty string should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Payment token is required"):
            validate_payment_token("")

    def test_whitespace_only_raises(self):
        """Whitespace-only token should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Payment token cannot be empty"):
            validate_payment_token("   ")

    def test_non_string_raises(self):
        """Non-string token should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Payment token must be a string"):
            validate_payment_token(12345)  # type: ignore


class TestValidateOrderItems:
    """Tests for validate_order_items function."""

    def test_valid_items(self):
        """Valid items list should not raise."""
        mock_product = MagicMock()
        items = [{"product": mock_product, "quantity": 2}]
        validate_order_items(items)

    def test_none_items_raises(self):
        """None items should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Order must have at least one item"):
            validate_order_items(None)

    def test_empty_list_raises(self):
        """Empty list should raise InvalidOrderError."""
        with pytest.raises(InvalidOrderError, match="Order must have at least one item"):
            validate_order_items([])

    def test_missing_product_raises(self):
        """Item without product should raise InvalidOrderError."""
        items = [{"quantity": 1}]
        with pytest.raises(InvalidOrderError, match="Item 1 must have a product"):
            validate_order_items(items)

    def test_zero_quantity_raises(self):
        """Item with zero quantity should raise InvalidOrderError."""
        mock_product = MagicMock()
        items = [{"product": mock_product, "quantity": 0}]
        with pytest.raises(InvalidOrderError, match="Item 1 quantity must be at least 1"):
            validate_order_items(items)

    def test_negative_quantity_raises(self):
        """Item with negative quantity should raise InvalidOrderError."""
        mock_product = MagicMock()
        items = [{"product": mock_product, "quantity": -1}]
        with pytest.raises(InvalidOrderError, match="Item 1 quantity must be at least 1"):
            validate_order_items(items)

    def test_default_quantity_is_one(self):
        """Item without quantity should default to 1 and pass."""
        mock_product = MagicMock()
        items = [{"product": mock_product}]
        validate_order_items(items)  # Should not raise


# =============================================================================
# OrderService Tests
# =============================================================================


class TestOrderServiceCalculateTotal:
    """Tests for OrderService.calculate_total method."""

    def test_single_item(self):
        """Calculate total for single item."""
        mock_product = MagicMock()
        mock_product.price = Decimal("25.00")

        service = OrderService()
        items = [{"product": mock_product, "quantity": 2}]

        total = service.calculate_total(items)

        assert total == Decimal("50.00")

    def test_multiple_items(self):
        """Calculate total for multiple items."""
        product1 = MagicMock()
        product1.price = Decimal("10.00")
        product2 = MagicMock()
        product2.price = Decimal("15.50")

        service = OrderService()
        items = [
            {"product": product1, "quantity": 2},
            {"product": product2, "quantity": 1},
        ]

        total = service.calculate_total(items)

        assert total == Decimal("35.50")

    def test_empty_items_raises(self):
        """Empty items should raise InvalidOrderError."""
        service = OrderService()

        with pytest.raises(InvalidOrderError):
            service.calculate_total([])

    def test_default_quantity(self):
        """Item without quantity should use default of 1."""
        mock_product = MagicMock()
        mock_product.price = Decimal("30.00")

        service = OrderService()
        items = [{"product": mock_product}]

        total = service.calculate_total(items)

        assert total == Decimal("30.00")


# =============================================================================
# StripeGateway Tests
# =============================================================================


class TestStripeGateway:
    """Tests for StripeGateway."""

    @patch("apps.order.gateways.stripe.stripe")
    def test_charge_success(self, mock_stripe):
        """Successful charge returns charge ID."""
        mock_charge = MagicMock()
        mock_charge.id = "ch_test123"
        mock_stripe.Charge.create.return_value = mock_charge

        gateway = StripeGateway()
        result = gateway.charge(
            amount=Decimal("50.00"),
            token="tok_visa",
            description="Test charge",
        )

        assert result == "ch_test123"
        mock_stripe.Charge.create.assert_called_once_with(
            amount=5000,  # cents
            currency="USD",
            description="Test charge",
            source="tok_visa",
        )

    @patch("apps.order.gateways.stripe.stripe")
    def test_charge_card_error(self, mock_stripe):
        """Card error raises PaymentError."""
        from stripe import CardError

        mock_stripe.Charge.create.side_effect = CardError(
            message="Card declined",
            param=None,
            code=None,
            http_body=None,
            http_status=None,
            headers=None,
        )

        gateway = StripeGateway()

        with pytest.raises(PaymentError, match="Card declined"):
            gateway.charge(
                amount=Decimal("50.00"),
                token="tok_declined",
                description="Test charge",
            )

    @patch("apps.order.gateways.stripe.stripe")
    def test_charge_stripe_error(self, mock_stripe):
        """Generic Stripe error raises PaymentError."""
        from stripe import StripeError

        mock_stripe.Charge.create.side_effect = StripeError("Connection error")

        gateway = StripeGateway()

        with pytest.raises(PaymentError, match="Payment failed"):
            gateway.charge(
                amount=Decimal("50.00"),
                token="tok_visa",
                description="Test charge",
            )

    def test_charge_invalid_amount_raises(self):
        """Invalid amount raises InvalidOrderError."""
        gateway = StripeGateway()

        with pytest.raises(InvalidOrderError):
            gateway.charge(
                amount=Decimal("-10.00"),
                token="tok_visa",
            )

    def test_charge_invalid_token_raises(self):
        """Invalid token raises InvalidOrderError."""
        gateway = StripeGateway()

        with pytest.raises(InvalidOrderError):
            gateway.charge(
                amount=Decimal("50.00"),
                token="",
            )


# =============================================================================
# Endpoint Tests (Smoke Tests)
# =============================================================================


@pytest.mark.django_db
class TestOrderEndpoints:
    """Basic smoke tests for order endpoints."""

    def test_checkout_requires_auth(self, client):
        """Test that checkout endpoint requires authentication."""
        response = client.post("/api/v1/checkout/")
        assert response.status_code in [401, 403]

    def test_orders_requires_auth(self, client):
        """Test that orders endpoint requires authentication."""
        response = client.get("/api/v1/orders/")
        assert response.status_code in [401, 403]
