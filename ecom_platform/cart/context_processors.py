from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
        cart_items_count = cart_items.count()
    else:
        session_id = request.session.session_key or request.session.create()
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
        cart_items = cart.cartitem_set.all()
        cart_items_count = cart_items.count()

    return {
        'cart_items': cart_items,
        'cart_items_count': cart_items_count
    }
