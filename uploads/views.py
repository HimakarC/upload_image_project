from io import BytesIO
from datetime import timedelta

from PIL import Image

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.files.base import ContentFile
from django.db.models import Q, Sum
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.utils import timezone

from .forms import ImageUploadForm
from .models import UploadedImage


# =========================================================
# LOGIN
# =========================================================

class UserLoginView(LoginView):

    template_name = "uploads/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return "/dashboard/"


# =========================================================
# LOGOUT
# =========================================================

class UserLogoutView(LogoutView):

    next_page = "/login/"


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username:
            return render(
                request,
                "uploads/register.html",
                {"error": "Username is required."}
            )

        if not password:
            return render(
                request,
                "uploads/register.html",
                {"error": "Password is required."}
            )

        if password != confirm_password:
            return render(
                request,
                "uploads/register.html",
                {"error": "Passwords do not match."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "uploads/register.html",
                {"error": "Username already exists."}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("dashboard")

    return render(request, "uploads/register.html")


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    user_images = UploadedImage.objects.filter(user=request.user)

    total_images = user_images.count()

    total_storage = (
        user_images.aggregate(
            total=Sum("compressed_size")
        )["total"] or 0
    )

    month_start = timezone.now().replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    monthly_uploads = user_images.filter(
        uploaded_at__gte=month_start
    ).count()

    recent_images = user_images.order_by("-uploaded_at")[:6]

    return render(
        request,
        "uploads/dashboard.html",
        {
            "total_images": total_images,
            "total_storage": total_storage,
            "monthly_uploads": monthly_uploads,
            "recent_images": recent_images,
        }
    )


# =========================================================
# UPLOAD IMAGE
# =========================================================

@login_required
def upload_image(request):

    if request.method == "POST":

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():

            uploaded_file = form.cleaned_data["image"]
            original_size = uploaded_file.size

            image = Image.open(uploaded_file)
            original_format = image.format
            width, height = image.size

            compressed_buffer = BytesIO()

            if original_format in ["JPEG", "JPG"]:

                if image.mode in ["RGBA", "P"]:
                    image = image.convert("RGB")

                image.save(
                    compressed_buffer,
                    format="JPEG",
                    quality=85,
                    optimize=True
                )

                extension = "jpg"
                file_type = "JPEG"

            elif original_format == "PNG":

                image.save(
                    compressed_buffer,
                    format="PNG",
                    optimize=True
                )

                extension = "png"
                file_type = "PNG"

            elif original_format == "WEBP":

                image.save(
                    compressed_buffer,
                    format="WEBP",
                    quality=85
                )

                extension = "webp"
                file_type = "WEBP"

            else:

                if image.mode in ["RGBA", "P"]:
                    image = image.convert("RGB")

                image.save(
                    compressed_buffer,
                    format="JPEG",
                    quality=85,
                    optimize=True
                )

                extension = "jpg"
                file_type = "JPEG"

            compressed_buffer.seek(0)

            compressed_size = compressed_buffer.getbuffer().nbytes

            uploaded_image = form.save(commit=False)
            uploaded_image.user = request.user
            uploaded_image.original_filename = uploaded_file.name
            uploaded_image.file_type = file_type
            uploaded_image.original_size = original_size
            uploaded_image.compressed_size = compressed_size
            uploaded_image.width = width
            uploaded_image.height = height

            base_name = uploaded_file.name.rsplit(".", 1)[0]
            compressed_name = f"{base_name}.{extension}"

            uploaded_image.image.save(
                compressed_name,
                ContentFile(compressed_buffer.read()),
                save=False
            )

            uploaded_image.save()

            # THUMBNAIL
            thumbnail_image = Image.open(uploaded_image.image)
            thumbnail_image.thumbnail((400, 400))

            thumbnail_buffer = BytesIO()

            if file_type == "PNG":

                thumbnail_image.save(
                    thumbnail_buffer,
                    format="PNG",
                    optimize=True
                )

                thumbnail_extension = "png"

            elif file_type == "WEBP":

                thumbnail_image.save(
                    thumbnail_buffer,
                    format="WEBP",
                    quality=80
                )

                thumbnail_extension = "webp"

            else:

                if thumbnail_image.mode in ["RGBA", "P"]:
                    thumbnail_image = thumbnail_image.convert("RGB")

                thumbnail_image.save(
                    thumbnail_buffer,
                    format="JPEG",
                    quality=80,
                    optimize=True
                )

                thumbnail_extension = "jpg"

            thumbnail_buffer.seek(0)

            thumbnail_name = f"{base_name}_thumb.{thumbnail_extension}"

            uploaded_image.thumbnail.save(
                thumbnail_name,
                ContentFile(thumbnail_buffer.read()),
                save=True
            )

            return redirect("success")

    else:
        form = ImageUploadForm()

    return render(request, "uploads/upload.html", {"form": form})


# =========================================================
# SUCCESS
# =========================================================

@login_required
def success(request):
    return render(request, "uploads/success.html")


# =========================================================
# GALLERY
# =========================================================

@login_required
def gallery(request):

    images = UploadedImage.objects.filter(user=request.user)

    search = request.GET.get("search", "").strip()
    file_type = request.GET.get("file_type", "")
    date_filter = request.GET.get("date", "")
    sort = request.GET.get("sort", "newest")

    if search:
        images = images.filter(
            Q(original_filename__icontains=search)
        )

    if file_type:
        images = images.filter(file_type__iexact=file_type)

    if date_filter:

        now = timezone.now()

        if date_filter == "today":
            start_date = now - timedelta(days=1)

        elif date_filter == "week":
            start_date = now - timedelta(days=7)

        elif date_filter == "month":
            start_date = now - timedelta(days=30)

        else:
            start_date = None

        if start_date:
            images = images.filter(uploaded_at__gte=start_date)

    if sort == "oldest":
        images = images.order_by("uploaded_at")

    elif sort == "name":
        images = images.order_by("original_filename")

    elif sort == "size":
        images = images.order_by("-compressed_size")

    else:
        images = images.order_by("-uploaded_at")

    return render(
        request,
        "uploads/gallery.html",
        {
            "images": images,
            "search": search,
            "file_type": file_type,
            "date_filter": date_filter,
            "sort": sort,
        }
    )


# =========================================================
# DELETE IMAGE
# =========================================================

@login_required
def delete_image(request, image_id):

    image = get_object_or_404(
        UploadedImage,
        id=image_id,
        user=request.user
    )

    if request.method == "POST":

        if image.image:
            image.image.delete(save=False)

        if image.thumbnail:
            image.thumbnail.delete(save=False)

        image.delete()

    return redirect("gallery")