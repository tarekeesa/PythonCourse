from django.urls import path
from .views import CancelView, CreateStripeCheckoutSessionView, SuccessView

app_name = 'billing'


urlpatterns = [
    path("create-checkout-session/", CreateStripeCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),

    ]
