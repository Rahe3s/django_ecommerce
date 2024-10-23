from django.db import models
from django.utils.text import slugify
import uuid


class Category(models.Model):
    uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to='categories', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category,self).save(*args, **kwargs)

    class Meta:
        db_table = 'category'
        verbose_name = 'category'    

    def __str__(self):
        return self.category_name
        

class products(models.Model):
    uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    product_name = models.CharField( max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    product_description = models.TextField()

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(products,self).save(*args, **kwargs)

    class Meta:
        db_table = 'products'
        verbose_name = 'products'    

    def __str__(self):
        return self.product_name


class productImages(models.Model):
    product = models.ForeignKey("products",on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products/')