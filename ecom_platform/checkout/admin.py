from django.contrib import admin
from django.utils.html import format_html
from .models import Address, Order

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'city', 'country', 'state', 'postal_code', 'address_type', 'active']
    list_filter = ['country', 'state', 'city', 'active', 'address_type']
    search_fields = ['name', 'city', 'postal_code']
    list_editable = ['active']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'cart_details')
    readonly_fields = ['cart_details']

    def cart_details(self, obj):
        if obj.cart:
            return format_html(
                "Total Quantity: {}, Total Price: ${}",
                obj.cart.get_total_quantity(),
                obj.cart.get_total_price()
            )
        return "No Cart"

