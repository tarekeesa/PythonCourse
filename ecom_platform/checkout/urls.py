from django.urls import path
from .views import checkout_view, submit_order

app_name = 'checkout'


urlpatterns = [
    path('', checkout_view, name='checkout_view'),
    path('submit_order/', submit_order, name='submit_order'),
]
