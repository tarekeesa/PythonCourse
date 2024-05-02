from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ('email',)
    list_display = ('email', 'full_name', 'country', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'gender', 'country')
    search_fields = ('email', 'full_name', 'country', 'source')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': ('full_name', 'profile_picture', 'bio', 'age', 'gender', 'nationality', 'country', 'Passport_number', 'contact', 'source')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff')
        }),
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('full_name', 'profile_picture', 'bio', 'age', 'gender', 'nationality', 'country', 'Passport_number', 'contact', 'source')
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)

# Register the custom admin
admin.site.register(CustomUser,CustomUserAdmin)

# Unregister the Group model if not needed
admin.site.unregister(Group)
