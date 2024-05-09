from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from cart.models import Cart

User = get_user_model()

ADDRESS_TYPES = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
    ('both',"both"),
)

class Address(models.Model):
    user            = models.ForeignKey(User, null=True, blank=True ,on_delete=models.CASCADE)
    name            = models.CharField(max_length=120, null=True, blank=True, help_text='Shipping to? Who is it for?')
    nickname        = models.CharField(max_length=120, null=True, blank=True, help_text='Internal Reference Nickname')
    address_type    = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line    = models.CharField(max_length=120)
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default='United Arab Emarite')
    state           = models.CharField(max_length=120,null=True, blank=True)
    postal_code     = models.CharField(max_length=120)
    active      = models.BooleanField(default=True)


    class Meta:
        indexes = [
            models.Index(fields=['city', 'name']),  
        ]
    def __str__(self):
        if self.nickname:
            return str(self.nickname)
        return str(self.address_line)

    # def get_absolute_url(self):
    #     return reverse("address-update", kwargs={"pk": self.pk})

    def get_short_address(self):
        for_name = self.name 
        if self.nickname:
            for_name = "{} | {},".format( self.nickname, for_name)
        return "{for_name} {line1}, {city}".format(
                for_name = for_name or "",
                line1 = self.address_line,
                city = self.city
            ) 

    def get_address(self):
        return "{for_name}\n{line1}\n{city}\n{state}, {postal}\n{country}".format(
                for_name = self.name or "",
                line1 = self.address_line,
                city = self.city,
                state = self.state,
                postal= self.postal_code,
                country = self.country
            )
    

class Order(models.Model):
    BILLING_TYPES = (
    ('card', 'card'),
    ('cash_on_delivery', 'cash_on_delivery'),
    )
    user                    = models.ForeignKey(User, null=True, blank=True ,on_delete=models.CASCADE)
    shipping_address        = models.ForeignKey(Address, null=True, blank=True ,on_delete=models.CASCADE)
    email                   = models.EmailField()
    active                  = models.BooleanField(default=True)
    update                  = models.DateTimeField(auto_now=True)
    timestamp               = models.DateTimeField(auto_now_add=True)
    billing_type            = models.CharField(max_length=120, choices=BILLING_TYPES ,default='cash_on_delivery' ,null=True,blank=True)
    cart                    = models.OneToOneField(Cart, null=True, blank=True ,on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['user','cart','shipping_address','billing_type','email','active',]),
        ]
        



