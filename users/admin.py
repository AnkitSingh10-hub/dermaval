from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'mobile_number', 'is_staff', 'is_active')
    
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number', 'avatar')}),
        ('Location', {'fields': ('province', 'district', 'municipality', 'ward', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Verification', {'fields': ('is_phone_verified', 'is_email_verified')}),
    )

    # This configures the "Add User" page (when you click 'Add User')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'mobile_number')}),
    )

# Register the model with the customized admin class
admin.site.register(User, CustomUserAdmin)