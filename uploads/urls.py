from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    register,
    dashboard,
    upload_image,
    success,
    gallery,
    delete_image,
)


urlpatterns = [

    path(
        "login/",
        UserLoginView.as_view(),
        name="login"
    ),

    path(
        "logout/",
        UserLogoutView.as_view(),
        name="logout"
    ),

    path(
        "register/",
        register,
        name="register"
    ),

    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),

    path(
        "upload/",
        upload_image,
        name="upload"
    ),

    path(
        "success/",
        success,
        name="success"
    ),

    path(
        "gallery/",
        gallery,
        name="gallery"
    ),

    path(
        "delete/<int:image_id>/",
        delete_image,
        name="delete_image"
    ),

]