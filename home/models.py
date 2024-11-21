from django.db import models
import uuid

class Banner(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='banners/', blank=True, null=True)  # Optional
    position = models.CharField(max_length=20, choices=[('homepage', 'homepage'), 
                                                             ('shoppage', 'shoppage'), 
                                                             ('productpage', 'productpage'),
                                                             ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title