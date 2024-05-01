from django.contrib import admin
from .models import Category, Product
from mptt.admin import DraggableMPTTAdmin


class ProductAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('title', 'price', 'cost', 'featured', 'quantity', 'active', 'is_digital', 'created_at')
    
    # Make these fields searchable in the admin
    search_fields = ('title', 'description', 'slug')
    
    # Add filters for these fields in the admin
    list_filter = ('active', 'featured', 'is_digital', 'created_at')
    
    # Enable sorting by these fields
    ordering = ('title', 'price')

    # If you have specific methods or display logic, you can define them here
    # Example to display a boolean as a custom icon
    def active_status(self, obj):
        return 'Yes' if obj.active else 'No'
    active_status.short_description = 'Is Active?'

admin.site.register(Product, ProductAdmin)
admin.site.register(Category , DraggableMPTTAdmin) 
