from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from cart.models import Cart
from .models import Address, Order

User = get_user_model()

def checkout_view(request):
    user = request.user
    context = {}

    if user.is_authenticated:
        addresses = user.address_set.all()
        has_pre_address = addresses.count() > 0
        print('has_pre_address',has_pre_address)
        cart = get_object_or_404(Cart, user=user)  # Assumes user is linked directly to a cart

        # Fetch cart items
        cart_items = cart.cartitem_set.all()
        total_price = cart.get_total_price()
        total_quantity = cart.get_total_quantity()

        print('addresses',addresses)
        context = {
            'addresses': addresses,
            'cart_items': cart_items,
            'total_price': total_price,
            'total_quantity': total_quantity,
            'user': user,
            'has_pre_address': has_pre_address,
        }

    return render(request, 'checkout/checkout.html', context)


def checkout_forms(request):
    user = request.user

    if not user.is_authenticated:
        action = 'show_full_form'
    elif not user.address_set.filter(active=True, address_type='billing').exists():
        action = 'show_billing_address_form'
    elif not user.address_set.filter(active=True, address_type='shipping').exists():
        action = 'show_shipping_address_form'
    else:
        action = 'review_order'
    # print('action',action)

    return JsonResponse({'action': action})


@require_http_methods(["POST"])
@csrf_exempt  # Only for testing, otherwise use csrf token in your form
def submit_order(request):
    # Extract the data from the request
    data = request.POST
    user = request.user
    create_account = request.POST.get('createAccount') == 'yes'

    payment_method = data.get('paymentMethod')
    different_address = 'Address-1' in request.POST
    print('Different Address:', different_address)
    address_Id = data.get('addressId')

    print('user',user,'create_account',data.get('createNewAccount'),'different_address',different_address,'payment_method',payment_method,'data',data)
    # Handle user creation or identification
    if create_account and not user.is_authenticated:
        # Create a new user if "Create an account" is checked and user is not authenticated
        username = data.get('emailAddress')  # Consider more robust username generation and validation
        password = User.objects.make_random_password()
        user = User.objects.create_user(username=username, email=data.get('emailAddress'), password=password)
        print('create_account',user)
        # TODO send email verfication  
    elif not user.is_authenticated:
        # Create a guest user or handle as an anonymous order
        print('guest user')
        user = None  # Or handle it by creating a temporary guest user
    print('address_Id',address_Id)
    if not address_Id == 'null':
        billing_address= Address.objects.filter(id=address_Id).first()
    else:
        billing_address_data = {
            'user': user,
            'name': user.full_name if user else 'Guest User',
            'address_line': data.get('billingAddress'),
            'city': data.get('billingCity'),
            'country': data.get('billingCountry'),
            'state': data.get('billingState'),
            'postal_code': data.get('billingPostcode'),
            'address_type': 'both' if not different_address else 'billing',
        }
        billing_address = Address.objects.create(**billing_address_data)

    shipping_address=billing_address

    if different_address:
        # Create a separate shipping address
        shipping_address_data = {
            'user': user,
            'name': user.full_name if user else 'Guest User',
            'address_line': data.get('shippingAddress'),
            'city': data.get('shippingCity'),
            'country': data.get('shippingCountry'),
            'state': data.get('shippingState'),
            'postal_code': data.get('shippingPostcode'),
            'address_type': 'shipping',
        }
        shipping_address = Address.objects.create(**shipping_address_data)

    # Optionally create an order instance
    order = Order.objects.create(
        user=user,
        email=data.get('emailAddress') or user.email,
        billing_type=payment_method,
        shipping_address=shipping_address
        # Other order fields as necessary
    )

    # Return a JSON response
    return JsonResponse({'status': 'success', 'message': 'Order processed successfully!', 'order_id': order.pk})
