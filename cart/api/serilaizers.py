from rest_framework import serializers
from cart.models import CartItem
from catalog.models import Product

class AddToCartSerializer(serializers.Serializer):
    product= serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity= serializers.IntegerField(min_value=1)

class CartItemSerializer(serializers.ModelSerializer):
    product_name= serializers.CharField(source="product.name", read_only= True)

    class Meta:
        model= CartItem
        fields= [
            "id",
            "product",
            "product_name",
            "quantity",
        ]

class UpdateCartItemSerializer(serializers.Serializer):
    quantity= serializers.IntegerField(min_value=1)