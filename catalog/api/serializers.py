from rest_framework import serializers
from catalog.models import Category, Product
from catalog.services.category_service import CategoryService
from catalog.services.product_service import ProductService

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields= [
            "id",
            "name"
        ]
    def create(self, validated_data):
        return CategoryService.create_category(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "stock",
            "created_at",
            "updated_at",
            "category",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]
    # product validations
    def validate_price(self,value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0"
            )
        return value
    def validate_stock(self,value):
        if value < 0:
            raise serializers.ValidationError(
                "Stock cannot be negative"
            )
        return value
            
    def validate_name(self,value):
        if not value.strip():
            raise serializers.ValidationError(
                "Name cannot be empty"
            )
        return value
            
    def create(self, validated_data):
        return ProductService.create_product(validated_data)
    