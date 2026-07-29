from django.db import models
from django.contrib.auth.models import User


class UploadedImage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_images'
    )

    image = models.ImageField(upload_to='uploads/')

    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=True
    )

    original_filename = models.CharField(
        max_length=255,
        blank=True
    )

    file_type = models.CharField(
        max_length=50,
        blank=True
    )

    original_size = models.PositiveIntegerField(
        default=0,
        help_text="Original file size in bytes"
    )

    compressed_size = models.PositiveIntegerField(
        default=0,
        help_text="Compressed file size in bytes"
    )

    width = models.PositiveIntegerField(
        default=0
    )

    height = models.PositiveIntegerField(
        default=0
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'images'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.original_filename} - {self.user.username}"

    @property
    def compression_percentage(self):
        if self.original_size == 0:
            return 0

        return round(
            ((self.original_size - self.compressed_size)
             / self.original_size) * 100,
            2
        )