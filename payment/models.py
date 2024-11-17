from django.db import models
from accounts.models import User_Details 
from orders.models import Address,Coupons
from product.models import ProductVariant
from decimal import Decimal
import uuid

class Order(models.Model):
    # Unique identifier for the order
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    user = models.ForeignKey(User_Details, on_delete=models.CASCADE, null=True, blank=True, related_name='order')# Linking to the user who placed the order
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey(Coupons, null=True, blank=True, on_delete=models.SET_NULL)  # Linking to a coupon if applied
    cart_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Total order amount
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Discount applied
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Final payable amount
    
    payment_method = models.CharField(max_length=20, choices=[('credit_card', 'Credit Card'), 
                                                             ('paypal', 'PayPal'), 
                                                             ('cod', 'Cash on Delivery')],
                                      default='cod')  # Payment method selected
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), 
                                                             ('paid', 'Paid'), 
                                                             ('failed', 'Failed')],
                                      default='pending')  # Status of the payment
    
    order_status = models.CharField(max_length=20, choices=[('processing', 'Processing'), 
                                                            ('shipped', 'Shipped'),
                                                            ('delivered', 'Delivered'),
                                                            ('cancelled', 'Cancelled')],
                                    default='processing')  # Order status
    
    created_at = models.DateTimeField(auto_now_add=True)  # Time of order creation
    updated_at = models.DateTimeField(auto_now=True)  # Time of last order update

    def __str__(self):
        return f"Order #{self.uid} - {self.user}"
    
class OrderItem(models.Model):
    # Unique identifier for the order item
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Linking to the order
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)  # Linking to the product variant (e.g., size, color)
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product ordered
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per item
    
    

    def __str__(self):
        return f"{self.product_variant.product.name} (x{self.quantity})"