from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name= models.CharField(max_length=100)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    description= models.TextField()
    stock= models.PositiveIntegerField(default=0)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

