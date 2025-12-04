from django.urls import path
from .views import (
    CartDetailView, AddToCartView, RemoveFromCartView,
    UpdateCartItemQuantityView, CheckoutView
)

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart-detail"),
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/remove/<int:product_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("cart/update-quantity/", UpdateCartItemQuantityView, name="update-cart-quantity"),
    path("orders/checkout/", CheckoutView, name="checkout"),
]
