from catalog.models import Product
from cart.models import Cart, CartItem

class CartRepository:

    @staticmethod
    def get_or_create_cart(user):
        cart, created= Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def get_product_for_update(product_id):
        return Product.objects.select_for_update().get(id=product_id)

    @staticmethod
    def get_or_create_cart_item(cart,product, quantity):
        cart_item, created= CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        return cart_item, created

    @staticmethod
    def get_cart(user):
        return Cart.objects.prefetch_related("items__product").get(user=user)

    @staticmethod
    def get_cart_item(cart,item_id):
        return CartItem.objects.select_related("product").get(id=item_id, cart=cart)