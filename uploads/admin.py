from django.contrib import admin
from .models import UploadedImage


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'original_filename',
        'user',
        'file_type',
        'original_size',
        'compressed_size',
        'width',
        'height',
        'uploaded_at',
    )

    list_filter = (
        'file_type',
        'uploaded_at',
    )

    search_fields = (
        'original_filename',
        'user__username',
    )

    readonly_fields = (
        'uploaded_at',
        'original_size',
        'compressed_size',
        'width',
        'height',
    )