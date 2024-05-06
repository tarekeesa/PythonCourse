from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )

    full_name = models.CharField(_('full_name'), max_length=50, blank=True)
    profile_picture = models.ImageField(
        _('profile picture'), upload_to='path/to/upload/', null=True, blank=True
    )
    bio = models.TextField(_('Bio'), max_length=500, blank=True)
    source = models.CharField(_('source'), max_length=75, blank=True)
    contact = models.CharField(_('contact'), max_length=50, blank=True, null=True)
    age = models.PositiveIntegerField(default=18)
    country = CountryField(blank_label='(select country)', blank=True, null=True)
    Passport_number = models.CharField(_('Official ID'), max_length=50, null=True, blank=True)
    gender = models.CharField(_('Gender'), max_length=20, choices=GENDER, default='male')
    nationality = CountryField(blank_label='(select country)', blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'username', 'bio', 'source', 'contact', 'full_name', 'country', 'gender', 'nationality']),
        ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'username', 'contact', 'country']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name if self.full_name else self.email

    def get_short_name(self):
        return self.email



class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
