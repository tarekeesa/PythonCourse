from django import template
from cart.models import Cart

register = template.Library()

@register.filter
def in_cart(product_id, user):
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            return cart.cartitem_set.filter(product_id=product_id).exists()
    return False
from django import template
from cart.models import Cart

register = template.Library()

@register.filter
def in_cart(product_id, user):
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            return cart.cartitem_set.filter(product_id=product_id).exists()
    return False
