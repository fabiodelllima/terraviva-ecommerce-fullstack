"""
Order views - Controller layer.

Thin controllers that delegate business logic to services.
"""

from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import MyOrderSerializer, OrderSerializer
from .services import OrderService, PaymentError


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    """
    Process checkout and create order.

    Validates input, delegates to OrderService for business logic.
    """
    serializer = OrderSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        order_service = OrderService()
        order = order_service.process_checkout(
            user=request.user,
            validated_data=serializer.validated_data,
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    except PaymentError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    """List orders for authenticated user."""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
