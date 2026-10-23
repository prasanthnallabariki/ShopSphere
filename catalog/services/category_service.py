from catalog.repositories.category_repository import CategoryRepository

class CategoryService:

    @staticmethod
    def create_category(validated_data):
        return CategoryRepository.create_category(validated_data)

    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all_categories()

    @staticmethod
    def get_category_by_id(category_id):
        return CategoryRepository.get_category_by_id(category_id)
