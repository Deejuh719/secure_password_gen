from django.contrib import admin
from .models import Password

# Register your models here.

class PasswordAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'app_name', 'url', 'username', 'app_pass', 'created_at', 'updated_at')
    list_filter = ('user_id', 'app_name', 'url', 'username', 'app_pass', 'created_at', 'updated_at')
    search_fields = ('user_id', 'app_name', 'url', 'username', 'app_pass', 'created_at', 'updated_at')
    ordering = ('user_id', 'username', 'app_name', 'created_at')

admin.site.register(Password, PasswordAdmin)