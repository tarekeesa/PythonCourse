from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth import get_user_model
from django.db.models import Q
import os, random
from mptt.models import MPTTModel, TreeForeignKey
from ecommerce.utils import unique_slug_generator, get_filename, upload_image_path
from django.db.models import Count


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
    category = TreeForeignKey('Category',null=True,blank=True,on_delete=models.CASCADE,related_query_name='products')

    objects = ProductManager()

    class Meta:
        indexes = [
            models.Index(fields=['title','store','active','featured','price','unit','cost','quantity','descriptions', 'is_digital','slug','created_at','category']),
        ]


class CategoryManager(models.Manager):
    def get_queryset(self):
        # Annotate each category with the count of its products
        return super().get_queryset().annotate(product_count=Count('products'))

    
class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, null=True, blank=True , on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True,
    related_name='children',
    db_index=True ,on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)

    objects = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'

    def inefficient_product_count(self):
        # This counts products by making a database query each time the method is called
        print('category',self.product_set.all())
        return self.product_set.count()
    
    def efficient_product_count(self):
        return getattr(self, 'product_count', 0)

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs
    
    def __str__(self):
        return self.name
        
    @property
    def title(self):
        return self.name