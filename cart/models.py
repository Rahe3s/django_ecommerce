from django.db import models
import uuid
from accounts.models import User_Details 
from product.models import ProductVariant 

class Cart(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User_Details, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.uid} for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.product.product_name} ({self.product_variant.size}, {self.product_variant.color})"
