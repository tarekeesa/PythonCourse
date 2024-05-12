from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Card(models.Model):
    stripe_id               = models.CharField(max_length=120)
    brand                   = models.CharField(max_length=120, null=True, blank=True)
    country                 = models.CharField(max_length=20, null=True, blank=True)
    exp_month               = models.IntegerField(null=True, blank=True)
    exp_year                = models.IntegerField(null=True, blank=True)
    last4                   = models.CharField(max_length=4, null=True, blank=True)
    default                 = models.BooleanField(default=True)
    active                  = models.BooleanField(default=True)
    timestamp               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)

    class Meta:
        indexes = [
            models.Index(fields=['stripe_id','active']),     
        ]


class Charge(models.Model):
    user                    = models.ForeignKey(User,on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    paid                    = models.BooleanField(default=False)
    refunded                = models.BooleanField(default=False)
    outcome                 = models.TextField(null=True, blank=True)
    outcome_type            = models.CharField(max_length=120, null=True, blank=True)
    seller_message          = models.CharField(max_length=120, null=True, blank=True)
    risk_level              = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['stripe_id','paid','seller_message']),
            
        ]