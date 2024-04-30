from django.db import models
from django_quill.fields import QuillField


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    cost = models.PositiveIntegerField(default=50)
    qr_image = models.ImageField(upload_to="image",null=True,blank=True)
    featured = models.BooleanField(default=False)
    quantity = models.IntegerField(blank=False,default=1)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    is_digital = models.BooleanField(default=False)
    descriptions = QuillField(blank=True,null=True)

    description=models.CharField(max_length=500,null=True)
    created_at=models.DateTimeField(auto_now=True,null=True) 
        