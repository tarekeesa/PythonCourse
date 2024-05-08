from django.urls import path
from .views import checkout_forms, checkout_view

app_name = 'checkout'


urlpatterns = [
    path('', checkout_view, name='checkout_view'),
    path('checkout_forms/', checkout_forms, name='checkout_forms'),

    
]