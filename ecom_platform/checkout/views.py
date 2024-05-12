from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import random
from cart.models import Cart, CartItem
from .models import Address, Order

User = get_user_model()

def checkout_view(request):
    user = request.user
    context = {}

    if user.is_authenticated:
        addresses = user.address_set.all()
        has_pre_address = addresses.count() > 0
        print('has_pre_address',has_pre_address)
        cart = get_object_or_404(Cart, user=user,active=True)  # Assumes user is linked directly to a cart

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
    else:
        session_id = request.session.session_key or request.session.create()
        cart = Cart.objects.get(session_id=session_id)
        cart_items = cart.cartitem_set.all()
        
        total_price = cart.get_total_price()
        total_quantity = cart.get_total_quantity()
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'total_quantity': total_quantity,
            'user': '',
            'has_pre_address': '',
        }
    if cart_items.count() <= 0:
        return redirect('products:list')


    return render(request, 'checkout/checkout.html', context)

def generate_unique_username(full_name):
    """ Generate a unique username by appending a random number. """
    return f"{full_name}_{random.randint(1000, 9999)}"

@require_http_methods(["POST"])
@csrf_exempt
def submit_order(request):
    # Extract the data from the request
    data = request.POST
    user = request.user
    create_account = request.POST.get('createAccount') == 'yes'
    payment_method = data.get('paymentMethod')
    different_address = 'Address-1' in request.POST
    address_Id = data.get('addressId')

    print('user',user,'create_account',data.get('createNewAccount'),'different_address',different_address,'payment_method',payment_method,'data',data)
    # Handle user creation or identification
    cart, _ = Cart.objects.new_or_get(request)
    if not user.is_authenticated:
        session_id = request.session.session_key or request.session.create()
        password = User.objects.make_random_password()
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        full_name = f'{first_name} {last_name}'
        company = data.get('companyName')
        mobile = data.get('mobile')
        email_address = data.get('emailAddress')
        try:
            if create_account:
                user = User.objects.create_user(username=generate_unique_username,full_name=full_name,contact=mobile,source=company, email=email_address, password=password,user_type='permenet')
                print('create_account',user)
                # TODO send email verfication  
            elif not user.is_authenticated:
                user = User.objects.create_user(username=generate_unique_username,full_name=full_name,contact=mobile,source=company, email=email_address, password=password,user_type='guest')
        except IntegrityError as e:
            print('IntegrityError',e)
            return JsonResponse({'status': 'error', 'message': 'A user with that email already exists.'})
        except Exception as e:
            print('error',e)
            return JsonResponse({'status': 'error', 'message': str(e)})

    print('address_Id',address_Id)
    if not address_Id == 'null':
        billing_address = Address.objects.filter(id=address_Id).first()

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
    print('billing_address',billing_address)

    shipping_address=billing_address
    print('shipping_address',shipping_address)

    if different_address:
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

    # The use of Django's transaction.atomic() ensures that either all parts of the order are successfully processed, 
    # or none are (in case of any error), which helps maintain data integrity
    print('cart','shipping_address',cart,shipping_address)
    if cart and shipping_address:

        order = Order.objects.create(
            user=user,
            email=data.get('emailAddress') or user.email,
            billing_type=payment_method,
            shipping_address=shipping_address,
            cart=cart,
            status='pending',
        )

    else:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'success', 'message': 'Order processed successfully!', 'order_id': order.pk})
