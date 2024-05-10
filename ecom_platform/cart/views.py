from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required


@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    product = Product.objects.get(id=product_id)

    # Get cart by session key if user is not authenticated
    cart, created = Cart.objects.new_or_get(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'price': product.price})

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({'message': 'Item added successfully', 'cart_count': cart.cartitem_set.count()})


def view_cart(request):
    # Retrieve cart based on session or user
    cart, created = Cart.objects.new_or_get(request)
    cart_items = cart.cartitem_set.all()
    total_price = cart.get_total_price()
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


@require_POST
@csrf_exempt
def update_cart_item(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity'))
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity = quantity
    cart_item.save()

    cart = cart_item.cart
    item_total = cart_item.get_total_price()
    cart_count = cart.cartitem_set.count()

    return JsonResponse({
        'cart_count': cart_count,
        'subtotal': cart.get_total_price(),
        'total': cart.get_total_price() + 3.00,
        'item_total': float(item_total)
    })

@require_POST
@csrf_exempt
def remove_cart_item(request):
    item_id = request.POST.get('item_id')
    cart_item = CartItem.objects.get(id=item_id)
    cart = cart_item.cart
    cart_item.delete()
    cart_count = Cart.objects.get(user=request.user).cartitem_set.count()  # Update count after removal

    return JsonResponse({
        'success': True,
        'cart_count': cart_count,
        'subtotal': cart.get_total_price(),
        'total': cart.get_total_price() + 3
    })


@require_POST
@login_required
def remove_from_cart(request):
    product_id = request.POST.get('product_id')
    print('product_id',product_id)
    item = CartItem.objects.get(product__id=product_id)
    if item.cart.user == request.user:  # Check ownership
        item.delete()
        cart_count = Cart.objects.get(user=request.user).cartitem_set.count()  # Update count after removal
        return JsonResponse({'success': True, 'cart_count': cart_count, 'message': 'Item removed successfully'})
    else:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)