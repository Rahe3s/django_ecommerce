from django.db import models
import uuid
from accounts.models import User_Details 

class Coupons(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)  # Specify max_length
    description = models.TextField()
    min_amount = models.IntegerField()
    discount = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coupons'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return f"Coupon {self.name} (UID: {self.uid})"
    


class Address(models.Model):
    user = models.ForeignKey(User_Details, on_delete=models.CASCADE, null=True, blank=True, related_name='addresses')
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    PIN = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.name} - {self.address}"
