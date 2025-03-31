from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    lsit_display = ['id', 'user', 'file', 'file_name', 'uploaded_at', 'size', 'special_link']
    readonly_fields = ['id']
    list_filter = ['user', 'file_name', 'uploaded_at', 'size']
