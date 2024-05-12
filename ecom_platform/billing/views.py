import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from cart.models import Cart
from checkout.models import Order
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

# Use SSL (HTTPS) for your webhook URL.
# Validate the Stripe signature for every webhook event to ensure its authenticity.
# Consider limiting access to the webhook URL to only Stripe's IPs.

class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def get(self, request, *args, **kwargs):
        try:
            cart, _ = Cart.objects.new_or_get(request)
            print('cart',cart)
            cart_items = cart.cartitem_set.all()
        except Cart.DoesNotExist:
            # Handle the case where the cart does not exist
            return redirect('some_error_view')
        
        order = Order.objects.get(cart=cart)

        line_items = [
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(item.product.price * 100),  # Price in cents
                    "product_data": {
                        "name": item.product.title,
                        "description": item.product.descriptions,
                        "images": [f"{settings.BACKEND_DOMAIN}{item.product.image.url}"],
                    },
                },
                "quantity": int(item.quantity),
            }
            for item in cart_items
        ]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            metadata={"order_id": order.id,
                      'session_id':'session_id={CHECKOUT_SESSION_ID}'},  # Assuming you have the order ID available here
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )

        return redirect(checkout_session.url)

        
class SuccessView(TemplateView):
    template_name = "billing/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get('session_id')
        if session_id:
            session = stripe.checkout.Session.retrieve(session_id)
            context['order_id'] = session.metadata.order_id
            # Optionally fetch more information about the order based on order_id
            print('session.metadata.order_id',session.metadata.order_id)
            order = Order.objects.get(id=session.metadata.order_id)
            order.status = 'paid'
            order.billing_id = session.metadata
            order.save()
            cart = order.cart
            cart.active=False
            cart.save()
        return context
    
class CancelView(TemplateView):
    template_name = "billing/cancel.html"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            session_id = self.request.GET.get('session_id')
            if session_id:
                session = stripe.checkout.Session.retrieve(session_id)
                context['order_id'] = session.metadata.order_id
                # Optionally fetch more information about the order based on order_id
                print('session.metadata.order_id',session.metadata.order_id)
                order = Order.objects.get(id=session.metadata.order_id)
                order.status = 'canceled'
                order.billing_id = session.metadata
                order.save()
            return context
    