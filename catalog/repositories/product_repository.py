from catalog.models import Product


class ProductRepository:

    @staticmethod
    def create_product(validated_data):
        return Product.objects.create(**validated_data)

    # @staticmethod
    # def get_all_products():
    #     return Product.objects.select_related("category").all()

    @staticmethod
    def get_products(category_id= None, search= None, sort_by= None, order_by="asc"):
        products= Product.objects.select_related("category").all().order_by("id")
        if category_id:
            products= products.filter(category_id=category_id)
        if search:
            products= products.filter(name__icontains=search)
        allowed_sort_fields= [
            "name",
            "price",
            "stock",
            "created_at",
        ]
        if sort_by in allowed_sort_fields:
            if order_by == "desc":
                sort_by= f"-{sort_by}"
            products= products.order_by(sort_by)
        return products

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.select_related("category").get(id=product_id)
