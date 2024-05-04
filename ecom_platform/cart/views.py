from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem

def add_to_cart(request, product_id, quantity=1):
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity  # Now increments by provided quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Product added to cart successfully!")
    else:
        messages.error(request, "You need to login to add items to your cart.")
    return redirect('products:list')

def view_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
        total_price = cart.get_total_price()
        return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return redirect('users:login')

