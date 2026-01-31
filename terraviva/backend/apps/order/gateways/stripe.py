"""
Stripe payment gateway.

Infrastructure layer - handles external payment provider integration.
"""

import logging
from decimal import Decimal

import stripe
from django.conf import settings

from ..exceptions import PaymentError
from ..validators import validate_amount, validate_payment_token

logger = logging.getLogger(__name__)


class StripeGateway:
    """
    Gateway for Stripe payment processing.

    Encapsulates all Stripe-related logic, making it easier to:
    - Test with mocks
    - Switch payment providers
    - Handle payment errors consistently
    """

    def __init__(self) -> None:
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def charge(
        self,
        amount: Decimal,
        token: str,
        description: str = "Terra Viva Purchase",
    ) -> str:
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
        # Defensive programming - fail fast
        validate_amount(amount)
        validate_payment_token(token)

        logger.info(f"Processing payment: amount={amount}, description={description}")

        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),  # Stripe expects cents
                currency="USD",
                description=description,
                source=token,
            )
            logger.info(f"Payment successful: charge_id={charge.id}")
            return charge.id

        except stripe.error.CardError as e:
            logger.warning(f"Card declined: {e.user_message}")
            raise PaymentError(f"Card declined: {e.user_message}") from e

        except stripe.error.StripeError as e:
            logger.error(f"Payment failed: {str(e)}")
            raise PaymentError(f"Payment failed: {str(e)}") from e
