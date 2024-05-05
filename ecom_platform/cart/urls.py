# urls.py
from django.urls import path
from .views import add_to_cart, remove_cart_item, remove_from_cart, update_cart_item, view_cart


app_name = 'cart'

urlpatterns = [
    path('', view_cart, name='list'),
    path('update-item/', update_cart_item, name='update-cart-item'),
    path('remove-item/', remove_cart_item, name='remove-cart-item'),
    path('remove/', remove_from_cart, name='remove-from-cart'),
    path('add/', add_to_cart, name='add-to-cart'),

]
