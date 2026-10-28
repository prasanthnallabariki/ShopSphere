from django.urls import path
from .views import CheckoutView, OrderListView, OrderDetailView, OrderCancelView

urlpatterns=[
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", OrderListView.as_view(), name="order-list"),
    path("<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
    path("<int:order_id>/cancel/", OrderCancelView.as_view(), name="order-cancel"),
]