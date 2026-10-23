from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "stock")
    search_fields = ("name",)
    list_filter = ("category",)