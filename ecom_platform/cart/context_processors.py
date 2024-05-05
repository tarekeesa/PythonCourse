from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
        cart_items_count = cart_items.count()
    else:
        cart_items = []
        cart_items_count = 0

    return {
        'cart_items': cart_items,
        'cart_items_count': cart_items_count
    }
