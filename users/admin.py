from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import User




class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'total_xp', 'is_banned', 'created_at', )
    list_filter = ('is_banned', 'is_email_verified', 'language_choice')
    search_fields = ('username', 'email', 'phone_number')


admin.site.register(User, UserAdmin)


























