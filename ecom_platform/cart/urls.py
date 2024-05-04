# urls.py
from django.urls import path
from .views import add_to_cart, view_cart


app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('', view_cart, name='list'),
]
