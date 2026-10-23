from catalog.models import Category

class CategoryRepository:

    @staticmethod
    def create_category(validated_data):
        return Category.objects.create(**validated_data)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category_by_id(category_id):
        return Category.objects.get(id=category_id)

    