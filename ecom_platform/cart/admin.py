from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    can_delete = True
    show_change_link = True

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'get_total_quantity', 'get_total_price']
    search_fields = ['user__username', 'session_id']
    readonly_fields = ['get_total_price', 'get_total_quantity']
    inlines = [CartItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('cartitem_set')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'price', 'discount_amount', 'discount_percentage', 'get_total_price']
    list_filter = ['cart', 'product']
    search_fields = ['cart__id', 'product__name']
    readonly_fields = ['get_total_price']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('cart', 'product')
