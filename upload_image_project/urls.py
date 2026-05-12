from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Root URL → Login Page
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # Upload App URLs
    path('', include('uploads.urls')),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='uploads/login.html'
        ),
        name='login'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/login/'
        ),
        name='logout'
    ),
]

# Media Files
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)