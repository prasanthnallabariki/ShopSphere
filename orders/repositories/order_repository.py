from orders.models import Order, OrderItem

class OrderRepository:
    @staticmethod
    def create_order(user, total_amount):
        return Order.objects.create(user=user, total_amount=total_amount)

    @staticmethod
    def create_order_item(order, product, quantity, price):
        return OrderItem.objects.create(order=order, product=product, quantity=quantity, price= price)

    @staticmethod
    def get_order_by_id(order_id, user):
        return Order.objects.prefetch_related("items__product").get(id=order_id, user=user)

    @staticmethod
    def get_user_orders(user, status_filter=None, sort_by="-created_at"):
        orders= Order.objects.filter(user=user)
        if status_filter:
            orders= orders.filter(status=status_filter)
        allowed_sort_fields=[
            "created_at",
            "total_amount",
            "status"
        ]
        sort_field= sort_by.lstrip("-")
        if sort_field not in allowed_sort_fields:
            sort_by= "-created_at"
        return orders.prefetch_related("items__product").order_by(sort_by)

    @staticmethod
    def get_order_for_update(order_id, user):
        return Order.objects.select_for_update().get(id=order_id, user=user)