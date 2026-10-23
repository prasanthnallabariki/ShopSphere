from django.conf import settings
from django.db import models

from catalog.models import Product

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING= "PENDING", "Pending"
        CONFIRMED= "CONFIRMED", "Confirmed"
        CANCELLED= "CANCELLED", "Cancelled"
    
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status= models.CharField(max_length=20, choices= Status.choices, default= Status.PENDING)
    total_amount= models.DecimalField(max_digits=12, decimal_places=2)
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    def __str__(self):
        return f"Order#{self.id}"

class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete= models.CASCADE, related_name="items")
    product= models.ForeignKey(Product, on_delete= models.PROTECT)
    quantity= models.PositiveBigIntegerField()
    price= models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"