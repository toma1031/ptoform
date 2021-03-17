from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from potform.models import User

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions', 'is_employee', 'is_supervisor', 'is_hr')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )