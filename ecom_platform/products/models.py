from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth import get_user_model
from django.db.models import Q
import os, random


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(price__icontains=query) 
                   )
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):  # Product.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        # Product.objects == self.get_queryset()
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


User = get_user_model()
class Product(models.Model):
    PRICE_UNITS_CHOICES = (
        ('', 'Choose Product Unit'),
        ('kg', 'kg'),
        ('l','litre'),
        ('pcs','pcs'),
        ('gm','gm'),
        ('m2', 'm2'),
        ('m3', 'm3'),
        ('ml', 'ml'),
            ) 
    
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    cost = models.PositiveIntegerField(default=50)
    qr_image = models.ImageField(upload_to="image",null=True,blank=True)
    image = models.ImageField(
            upload_to=upload_image_path, null=True, blank=True) # TODO apply validators
    featured = models.BooleanField(default=False)
    quantity = models.IntegerField(blank=False,default=1)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    descriptions = QuillField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now=True,null=True) 
    is_digital = models.BooleanField(default=False)
    store   = models.CharField(max_length=120,null=True)
    likes = models.ManyToManyField(User, related_name='product_like')
    unit = models.CharField(max_length= 50,choices = PRICE_UNITS_CHOICES,default='')

    objects = ProductManager()

    class Meta:
        indexes = [
            models.Index(fields=['title','store','active','featured','unit', 'slug','created_at']),
        ]
    
