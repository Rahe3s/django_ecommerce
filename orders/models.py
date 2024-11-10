from django.db import models
import uuid

class Coupons(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)  # Specify max_length
    description = models.TextField()
    min_amount = models.IntegerField()
    discount = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Coupons'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return f"Coupon {self.name} (UID: {self.uid})"
