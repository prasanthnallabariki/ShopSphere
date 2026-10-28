from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError, NotFound
from orders.models import Order, OrderItem
from orders.repositories.order_repository import OrderRepository
from cart.models import Cart
from orders.tasks import process_order_notification

class OrderService:

    @staticmethod
    @transaction.atomic
    def checkout(user):
        cart= Cart.objects.prefetch_related("items__product").get(user=user)
        cart_items= cart.items.all()
        if not cart_items.exists():
            raise ValidationError("Cart is empty")
        total_amount= Decimal("0.00")
        for cart_item in cart_items:
            product= cart_item.product
            if cart_item.quantity > product.stock:
                raise ValidationError("Requested quantity exceeds available stock")
            total_amount+= cart_item.quantity * product.price
        order= OrderRepository.create_order(user=user, total_amount=total_amount)
        for cart_item in cart_items:
            product= cart_item.product
            OrderRepository.create_order_item(order=order, product=product, quantity= cart_item.quantity, price=product.price)
            product.stock-= cart_item.quantity
            product.save(update_fields=["stock"])
        cart.items.all().delete()
        transaction.on_commit(lambda: process_order_notification.delay(order.id))
        return order

    @staticmethod
    def get_user_orders(user, status_filter=None, sort_by="-created_at"):
        return OrderRepository.get_user_orders(user=user, status_filter=status_filter, sort_by=sort_by)

    @staticmethod
    def get_order(order_id, user):
        try:
            return OrderRepository.get_order_by_id(order_id, user)
        except Order.DoesNotExist:
            raise NotFound("Order not found")

    @staticmethod
    @transaction.atomic
    def cancel_order(order_id, user):
        order = OrderRepository.get_order_for_update(order_id, user)

        if order.status != Order.Status.PENDING:
            raise ValidationError("Only pending orders can be cancelled")

        items = order.items.select_related("product")

        for item in items:
            product = item.product.__class__.objects.select_for_update().get(
                pk=item.product_id
            )
            product.stock += item.quantity
            product.save(update_fields=["stock"])

        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])

        return order