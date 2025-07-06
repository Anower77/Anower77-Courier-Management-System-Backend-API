from django.urls import path
from .views import (
    UserOrderCreateView, UserOrderListView, DeliveryManOrdersView,
    UpdateOrderStatusView, AdminOrderListView, AssignDeliveryManView,
    CreatePaymentSessionView, APIRootView, stripe_webhook
)

urlpatterns = [
    path('user/create/', UserOrderCreateView.as_view()),
    path('user/orders/', UserOrderListView.as_view()),
    path('delivery/orders/', DeliveryManOrdersView.as_view()),
    path('delivery/status/<int:pk>/', UpdateOrderStatusView.as_view()),
    path('admin/orders/', AdminOrderListView.as_view()),
    path('admin/assign/<int:pk>/', AssignDeliveryManView.as_view()),
    path('payment/session/', CreatePaymentSessionView.as_view()),
    path('stripe/webhook/', stripe_webhook),
    path('api/v1/', APIRootView.as_view()),
]
