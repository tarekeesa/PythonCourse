from .models import Cart

def cart_context(request):
    cart, created = Cart.objects.new_or_get(request)
    cart_items = cart.cartitem_set.all()
    cart_items_count = cart_items.count()
    return {
        'cart_items': cart_items,
        'cart_items_count': cart_items_count
    }
