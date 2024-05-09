from django import template
from django.utils.http import url_has_allowed_host_and_scheme
from cart.models import Cart, CartItem
from django.db.models import Q

register = template.Library()

@register.filter
def in_cart(product_id, request):
    # Check if user is authenticated and get the cart accordingly
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        if session_id:
            cart = Cart.objects.filter(session_id=session_id).first()
        else:
            return False

    if cart:
        return CartItem.objects.filter(cart=cart, product_id=product_id).exists()
    return False
