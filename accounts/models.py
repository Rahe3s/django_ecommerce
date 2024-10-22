from django.db import models
from django.contrib.auth.models import AbstractUser

class User_Details(AbstractUser):
    username = None
    email = models.EmailField(unique=True,max_length=255)
    phone = models.CharField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 


    class Meta:
        db_table = 'user_profile'
        verbose_name = 'user profile'

    def __str__(self):
        return self.first_name
