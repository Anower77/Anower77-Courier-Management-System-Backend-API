import stripe
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import Order
from .serializers import OrderSerializer, AssignDeliverySerializer
from .permissions import IsAdmin, IsDeliveryMan
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Assign Delivery Man View
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

# stripe webhook
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()


class APIRootView(APIView):
    def get(self, request):
        return Response({
            "auth": "/api/v1/auth/",
            "orders": {
                "create": "/api/v1/orders/user/create/",
                "myOrders": "/api/v1/orders/user/orders/",
                "deliveryOrders": "/api/v1/orders/delivery/orders/",
                "updateStatus": "/api/v1/orders/delivery/status/<int:pk>/",
                "adminList": "/api/v1/orders/admin/orders/",
                "assign": "/api/v1/orders/admin/assign/<int:pk>/",
                "payment": "/api/v1/orders/payment/session/"
            }
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET 

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata']['order_id']

        try:
            order = Order.objects.get(id=order_id)
            order.is_paid = True
            order.save()
        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)


STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY")
DOMAIN_URL = config("DOMAIN_URL")



class CreatePaymentSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        order_id = request.data.get("order_id")
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=404)

        if order.is_paid:
            return Response({"message": "Order already paid"}, status=400)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Courier Order #{order.id}",
                        },
                        "unit_amount": int(order.cost * 100), 
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=settings.DOMAIN_URL + "/payment/success/",
            cancel_url=settings.DOMAIN_URL + "/payment/cancel/",
            metadata={
                "order_id": order.id
            }
        )

        return Response({"checkout_url": checkout_session.url})



# User Order Create View
class UserOrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
# User Order List View
class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# Delivery Man Orders View
class DeliveryManOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsDeliveryMan]

    def get_queryset(self):
        return Order.objects.filter(delivery_man=self.request.user)

# Update Order Status View
class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsDeliveryMan]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        if order.delivery_man != request.user:
            return Response({"message": "Unauthorized"}, status=403)
        order.status = request.data.get('status')
        order.save()
        return Response({"message": "Status updated", "data": OrderSerializer(order).data})


# Admin Order List View
class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


# Assign Delivery Man View
class AssignDeliveryManView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    serializer_class = AssignDeliverySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        delivery_man_id = request.data.get('delivery_man')

        try:
            delivery_man = User.objects.get(id=delivery_man_id, role='delivery')
        except User.DoesNotExist:
            raise ValidationError({'delivery_man': 'Delivery man not found or invalid role'})

        order.delivery_man = delivery_man
        order.save()

        return Response({
            "message": "Delivery man assigned successfully.",
            "data": OrderSerializer(order).data
        })
