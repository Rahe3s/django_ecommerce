from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid



# class BaseModel(models.Model):
#     uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
#     created_at = models.DateTimeField(auto_now= True)
#     updated_at = models.DateTimeField(auto_now_add= True)

#     class Meta:
#         abstract = True 


class User_Details(AbstractUser):
    uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    username = None
    email = models.EmailField(unique=True, max_length=255, null=True, blank=True)
    phone = models.CharField(unique=True)
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = [] 


    class Meta:
        db_table = 'user_profile'
        verbose_name = 'user profile'

    def __str__(self):
        return self.first_name
