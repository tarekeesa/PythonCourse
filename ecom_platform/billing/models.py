from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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