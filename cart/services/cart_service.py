from django.db import transaction
from rest_framework.exceptions import ValidationError
from cart.models import Cart, CartItem
from cart.repositories.cart_repository import CartRepository

class CartService:

    @staticmethod
    @transaction.atomic
    def add_item(user, product_id, quantity):
        cart = CartRepository.get_or_create_cart(user)
        product= CartRepository.get_product_for_update(product_id)
        if quantity > product.stock:
            raise ValidationError("Requested quantity exceeds available stock")
        cart_item, created = CartRepository.get_or_create_cart_item(cart, product, quantity)
        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                raise ValidationError("Total cart quantity exceeds available stock")
            cart_item.quantity = new_quantity
            cart_item.save(
                update_fields= ["quantity"]
            )
        return cart_item

    @staticmethod
    def get_cart(user):
        return CartRepository.get_cart(user)

    @staticmethod
    def update_item(user, item_id, quantity):
        cart= CartRepository.get_cart(user)
        cart_item= CartRepository.get_cart_item(cart, item_id)
        if quantity > cart_item.product.stock:
            raise ValidationError("Requested quanttiy exceeds available stock")
        cart_item.quantity= quantity
        cart_item.save(update_fields=["quantity"])
        return cart_item

    @staticmethod
    def remove_item(user, item_id):
        cart= CartRepository.get_cart(user)
        cart_item= CartRepository.get_cart_item(cart, item_id)
        cart_item.delete()