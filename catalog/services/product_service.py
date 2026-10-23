import logging
from catalog.repositories.product_repository import ProductRepository
from catalog.cache import invalidate_product_cache

logger = logging.getLogger("shopsphere")

class ProductService:

    @staticmethod
    def create_product(validated_data):
        logger.info("Creating product: %s", validated_data.get("name"))
        product =ProductRepository.create_product(validated_data)
        logger.info("Product created successfully. ID: %s", product.id)
        invalidate_product_cache()
        return product

    # @staticmethod
    # def get_all_products():
    #     return ProductRepository.get_all_products()

    @staticmethod
    def get_products(category_id= None, search= None, sort_by= None, order_by= "asc"):
        return ProductRepository.get_products(category_id= category_id, search= search, sort_by= sort_by, order_by= order_by)
    

    @staticmethod
    def get_product_by_id(product_id):
        return ProductRepository.get_product_by_id(product_id)
    