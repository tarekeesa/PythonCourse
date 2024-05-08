from django.shortcuts import render
from django.http import JsonResponse


def checkout_view(request):
    user = request.user

    if not user.is_authenticated:
        action = 'not_loggedin'
    else:
        if not user.address_set.filter(active=True).first():  # Assume a related object 'profile' exists
            action = 'no_billing_address'
        else:
            action = 'confim_shipping_address'
    
    context = {
        'ation': action
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
    print('action',action)

    return JsonResponse({'action': action})

