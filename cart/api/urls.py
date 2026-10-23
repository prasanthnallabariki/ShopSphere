from django.urls import path
from .views import AddToCartView, CartView, CartItemDetailView

urlpatterns = [
    path(
        "items/", AddToCartView.as_view(), name="add-to-cart"
    ),
    path("", CartView.as_view(), name="cart"),
    path("<int:item_id>/", CartItemDetailView.as_view(), name="cart-item-detail")
]