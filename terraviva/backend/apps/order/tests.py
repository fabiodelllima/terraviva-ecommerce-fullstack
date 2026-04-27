"""Tests for order app."""

from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth.models import User

from apps.order.exceptions import InvalidOrderError, PaymentError
from apps.order.gateways import StripeGateway
from apps.order.models import Order, OrderItem
from apps.order.services import OrderService
from apps.order.validators import (
    validate_amount,
    validate_order_items,
    validate_payment_token,
)
from apps.product.factories import ProductFactory

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


# =============================================================================
# OrderService.create_order
# =============================================================================


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="buyer",
        email="buyer@example.com",
        password="testpass123",
    )


@pytest.fixture
def order_data():
    """Return valid order field data."""
    return {
        "first_name": "Maria",
        "last_name": "Silva",
        "email": "maria@example.com",
        "address": "Rua Teste, 123",
        "zipcode": "01000-000",
        "place": "São Paulo",
        "phone": "11999998888",
        "stripe_token": "tok_visa",
        "paid_amount": Decimal("99.90"),
    }


@pytest.mark.django_db
class TestOrderServiceCreateOrder:
    """Tests for OrderService.create_order method."""

    def test_creates_order_with_user_and_data(self, user, order_data):
        """create_order must persist Order with user and provided fields."""
        product = ProductFactory(price=Decimal("50.00"))
        items_data = [{"product": product, "price": product.price, "quantity": 2}]

        service = OrderService()
        order = service.create_order(
            user=user,
            order_data=order_data,
            items_data=items_data,
        )

        assert order.pk is not None
        assert order.user == user
        assert order.first_name == "Maria"
        assert order.email == "maria@example.com"
        assert order.paid_amount == Decimal("99.90")

    def test_creates_order_items(self, user, order_data):
        """create_order must persist all OrderItems linked to the order."""
        product_a = ProductFactory(price=Decimal("10.00"))
        product_b = ProductFactory(price=Decimal("20.00"))
        items_data = [
            {"product": product_a, "price": product_a.price, "quantity": 1},
            {"product": product_b, "price": product_b.price, "quantity": 3},
        ]

        service = OrderService()
        order = service.create_order(
            user=user,
            order_data=order_data,
            items_data=items_data,
        )

        items = OrderItem.objects.filter(order=order)
        assert items.count() == 2
        assert items.filter(product=product_a, quantity=1).exists()
        assert items.filter(product=product_b, quantity=3).exists()

    def test_atomic_rollback_on_item_failure(self, user, order_data):
        """If item creation fails, the order must not be persisted."""
        valid_product = ProductFactory(price=Decimal("10.00"))
        # Second item is malformed (missing required FK), should raise
        items_data = [
            {"product": valid_product, "price": Decimal("10.00"), "quantity": 1},
            {"product": None, "price": Decimal("5.00"), "quantity": 1},
        ]

        service = OrderService()
        with pytest.raises(Exception):  # noqa: B017
            service.create_order(
                user=user,
                order_data=order_data,
                items_data=items_data,
            )

        assert Order.objects.count() == 0
        assert OrderItem.objects.count() == 0

    def test_creates_empty_order_when_no_items(self, user, order_data):
        """create_order with empty items_data still creates the order."""
        service = OrderService()
        order = service.create_order(
            user=user,
            order_data=order_data,
            items_data=[],
        )

        assert order.pk is not None
        assert OrderItem.objects.filter(order=order).count() == 0


# =============================================================================
# OrderService.process_checkout
# =============================================================================


@pytest.mark.django_db
class TestOrderServiceProcessCheckout:
    """Tests for OrderService.process_checkout orchestration."""

    def _make_validated_data(self, products_with_quantities):
        """Build a validated_data dict like the serializer would produce."""
        items = [{"product": p, "price": p.price, "quantity": q} for p, q in products_with_quantities]
        return {
            "first_name": "Maria",
            "last_name": "Silva",
            "email": "maria@example.com",
            "address": "Rua Teste, 123",
            "zipcode": "01000-000",
            "place": "São Paulo",
            "phone": "11999998888",
            "stripe_token": "tok_visa",
            "items": items,
        }

    def test_happy_path_creates_order_and_charges(self, user):
        """Successful flow: payment charged, order persisted with calculated total."""
        product = ProductFactory(price=Decimal("25.00"))
        validated_data = self._make_validated_data([(product, 2)])

        gateway = MagicMock(spec=StripeGateway)
        gateway.charge.return_value = "ch_test_success"

        service = OrderService(payment_gateway=gateway)
        order = service.process_checkout(user=user, validated_data=validated_data)

        gateway.charge.assert_called_once()
        call_kwargs = gateway.charge.call_args.kwargs
        assert call_kwargs["amount"] == Decimal("50.00")
        assert call_kwargs["token"] == "tok_visa"

        assert order.pk is not None
        assert order.paid_amount == Decimal("50.00")
        assert OrderItem.objects.filter(order=order).count() == 1

    def test_payment_failure_does_not_create_order(self, user):
        """If gateway raises PaymentError, order must not be persisted."""
        product = ProductFactory(price=Decimal("25.00"))
        validated_data = self._make_validated_data([(product, 1)])

        gateway = MagicMock(spec=StripeGateway)
        gateway.charge.side_effect = PaymentError("Card declined")

        service = OrderService(payment_gateway=gateway)

        with pytest.raises(PaymentError):
            service.process_checkout(user=user, validated_data=validated_data)

        assert Order.objects.count() == 0

    def test_invalid_items_raises_before_payment(self, user):
        """Invalid items raise InvalidOrderError before charging the gateway."""
        validated_data = self._make_validated_data([])  # empty items

        gateway = MagicMock(spec=StripeGateway)
        service = OrderService(payment_gateway=gateway)

        with pytest.raises(InvalidOrderError):
            service.process_checkout(user=user, validated_data=validated_data)

        gateway.charge.assert_not_called()
        assert Order.objects.count() == 0

    def test_paid_amount_uses_calculated_total(self, user):
        """paid_amount must come from calculate_total, not from payload."""
        product_a = ProductFactory(price=Decimal("10.00"))
        product_b = ProductFactory(price=Decimal("15.50"))
        validated_data = self._make_validated_data([(product_a, 2), (product_b, 1)])

        gateway = MagicMock(spec=StripeGateway)
        gateway.charge.return_value = "ch_ok"

        service = OrderService(payment_gateway=gateway)
        order = service.process_checkout(user=user, validated_data=validated_data)

        assert order.paid_amount == Decimal("35.50")

    def test_charge_description_includes_user_email(self, user):
        """Charge description must include the user's email for traceability."""
        product = ProductFactory(price=Decimal("10.00"))
        validated_data = self._make_validated_data([(product, 1)])

        gateway = MagicMock(spec=StripeGateway)
        gateway.charge.return_value = "ch_ok"

        service = OrderService(payment_gateway=gateway)
        service.process_checkout(user=user, validated_data=validated_data)

        call_kwargs = gateway.charge.call_args.kwargs
        assert user.email in call_kwargs["description"]


# =============================================================================
# E2E Tests: /api/v1/checkout/
# =============================================================================


@pytest.fixture
def authenticated_client(user):
    """Return an APIClient authenticated as the test user."""
    from rest_framework.test import APIClient

    client = APIClient()
    client.force_authenticate(user=user)
    return client


def _build_checkout_payload(product, quantity=1):
    """Build a valid checkout payload referencing an existing product."""
    return {
        "first_name": "Maria",
        "last_name": "Silva",
        "email": "maria@example.com",
        "address": "Rua Teste, 123",
        "zipcode": "01000-000",
        "place": "São Paulo",
        "phone": "11999998888",
        "stripe_token": "tok_visa",
        "items": [
            {
                "product": product.pk,
                "price": str(product.price),
                "quantity": quantity,
            }
        ],
    }


@pytest.mark.django_db
class TestCheckoutEndpoint:
    """E2E tests for /api/v1/checkout/ endpoint."""

    def test_unauthenticated_returns_401_or_403(self, client):
        """Unauthenticated request must be rejected with 401 or 403."""
        response = client.post("/api/v1/checkout/", {}, content_type="application/json")
        assert response.status_code in (401, 403)

    @patch("apps.order.views.OrderService")
    def test_valid_payload_returns_201(self, mock_service_cls, authenticated_client):
        """Valid payload with successful payment must return 201."""
        product = ProductFactory(price=Decimal("25.00"))
        payload = _build_checkout_payload(product, quantity=2)

        # Mock OrderService to avoid hitting Stripe
        mock_order = MagicMock()
        mock_order.pk = 1
        mock_order.id = 1
        mock_order.first_name = "Maria"
        mock_order.last_name = "Silva"
        mock_order.email = "maria@example.com"
        mock_order.address = "Rua Teste, 123"
        mock_order.zipcode = "01000-000"
        mock_order.place = "São Paulo"
        mock_order.phone = "11999998888"
        mock_order.stripe_token = "tok_visa"
        mock_order.items.all.return_value = []
        mock_service_cls.return_value.process_checkout.return_value = mock_order

        response = authenticated_client.post(
            "/api/v1/checkout/",
            payload,
            format="json",
        )

        assert response.status_code == 201
        mock_service_cls.return_value.process_checkout.assert_called_once()

    def test_invalid_payload_returns_400(self, authenticated_client):
        """Payload missing required fields must return 400 with serializer errors."""
        payload = {"first_name": "Maria"}  # missing everything else

        response = authenticated_client.post(
            "/api/v1/checkout/",
            payload,
            format="json",
        )

        assert response.status_code == 400
        # At least the required fields should be in the error response
        assert "last_name" in response.data
        assert "email" in response.data
        assert "items" in response.data

    def test_valid_payload_persists_order_in_database(self, authenticated_client, user):
        """Successful checkout must create Order and OrderItem rows."""
        product = ProductFactory(price=Decimal("30.00"))
        payload = _build_checkout_payload(product, quantity=2)

        with patch("apps.order.views.OrderService") as mock_service_cls:
            # Make the mocked service actually create an order using the real ORM
            def real_process_checkout(user, validated_data):
                from apps.order.services import OrderService as RealService

                gateway = MagicMock(spec=StripeGateway)
                gateway.charge.return_value = "ch_e2e_test"
                real_service = RealService(payment_gateway=gateway)
                return real_service.process_checkout(user=user, validated_data=validated_data)

            mock_service_cls.return_value.process_checkout.side_effect = real_process_checkout

            response = authenticated_client.post(
                "/api/v1/checkout/",
                payload,
                format="json",
            )

        assert response.status_code == 201
        assert Order.objects.count() == 1
        order = Order.objects.first()
        assert order is not None
        assert order.user == user
        assert order.paid_amount == Decimal("60.00")
        assert OrderItem.objects.filter(order=order).count() == 1

    @patch("apps.order.views.OrderService")
    def test_payment_error_returns_400_with_generic_message(self, mock_service_cls, authenticated_client):
        """PaymentError from service must produce 400 with generic user-safe message."""
        product = ProductFactory(price=Decimal("10.00"))
        payload = _build_checkout_payload(product)

        mock_service_cls.return_value.process_checkout.side_effect = PaymentError("Card declined: insufficient funds")

        response = authenticated_client.post(
            "/api/v1/checkout/",
            payload,
            format="json",
        )

        assert response.status_code == 400
        # User-facing error must not leak Stripe details
        assert "insufficient funds" not in str(response.data).lower()
        assert "error" in response.data
