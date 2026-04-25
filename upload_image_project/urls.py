from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # 👉 Root URL → Login page
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # 👉 App URLs
    path('', include('uploads.urls')),

    # 🔐 Authentication
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='uploads/login.html'),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/login/'),
        name='logout'
    ),
]

# 👉 Serve media files (uploaded images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)