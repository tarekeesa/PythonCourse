import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs["pk"])
        print('product',product)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(product.price) * 100,
                        "product_data": {
                            "name": product.title,
                            "description": product.descriptions,
                            "images": [
                                f"{settings.BACKEND_DOMAIN}/{product.image}"
                            ],
                        },
                    },
                    "quantity": product.quantity,
                }
            ],
            metadata={"product_id": product.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)
    
class SuccessView(TemplateView):
    template_name = "billing/success.html"

class CancelView(TemplateView):
    template_name = "billing/cancel.html"