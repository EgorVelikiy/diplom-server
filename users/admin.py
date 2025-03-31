from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    lsit_display = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']
    readonly_fields = ['id']
