from django.urls import path
from .views import (
    upload_image,
    success,
    gallery,
    delete_image,
    gallery_data,
    register
)

urlpatterns = [
    path('upload/', upload_image, name='upload'),   # 👈 changed
    path('success/', success, name='success'),
    path('gallery/', gallery, name='gallery'),
    path('gallery-data/', gallery_data, name='gallery_data'),
    path('delete/<int:image_id>/', delete_image, name='delete_image'),
    path('register/', register, name='register'),
]