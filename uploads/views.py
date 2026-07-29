from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db.models import Q, Sum, Count
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
import os

from .forms import ImageUploadForm
from .models import UploadedImage


# 🔐 Register
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'uploads/register.html', {'form': form})


# 📤 Upload Image
@login_required
def upload_image(request):

    if request.method == 'POST':
        form = ImageUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            uploaded_file = form.cleaned_data['image']

            # Open image
            image = Image.open(uploaded_file)

            # Convert RGBA/P to RGB for JPEG compatibility
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')

            original_size = uploaded_file.size

            # Store dimensions
            width, height = image.size

            # Compress image
            compressed_buffer = BytesIO()

            image.save(
                compressed_buffer,
                format='JPEG',
                quality=85,
                optimize=True
            )

            compressed_buffer.seek(0)

            compressed_size = compressed_buffer.getbuffer().nbytes

            # Create database object
            img = form.save(commit=False)

            img.user = request.user
            img.original_filename = uploaded_file.name
            img.file_type = image.format or 'JPEG'
            img.original_size = original_size
            img.compressed_size = compressed_size
            img.width = width
            img.height = height

            # Save compressed image
            base_name = uploaded_file.name.rsplit(
                '.',
                1
            )[0]

            compressed_name = (
                f"{base_name}.jpg"
            )

            img.image.save(
                compressed_name,
                ContentFile(
                    compressed_buffer.read()
                ),
                save=False
            )

            img.save()

            # Generate thumbnail
            image.thumbnail(
                (400, 400)
            )

            thumbnail_buffer = BytesIO()

            image.save(
                thumbnail_buffer,
                format='JPEG',
                quality=80,
                optimize=True
            )

            thumbnail_buffer.seek(0)

            thumbnail_name = (
                f"{base_name}_thumb.jpg"
            )

            img.thumbnail.save(
                thumbnail_name,
                ContentFile(
                    thumbnail_buffer.read()
                ),
                save=True
            )

            return redirect('success')

    else:
        form = ImageUploadForm()

    return render(
        request,
        'uploads/upload.html',
        {'form': form}
    )

# ✅ Success Page
@login_required
def success(request):
    return render(request, 'uploads/success.html')


# 🖼️ Gallery Page
@login_required
def gallery(request):

    images = UploadedImage.objects.filter(
        user=request.user
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    file_type = request.GET.get(
        'file_type',
        ''
    )

    date_filter = request.GET.get(
        'date',
        ''
    )

    sort = request.GET.get(
        'sort',
        'newest'
    )

    # Search by filename
    if search:
        images = images.filter(
            Q(original_filename__icontains=search)
        )

    # Filter by file type
    if file_type:
        images = images.filter(
            file_type__iexact=file_type
        )

    # Date filtering
    if date_filter:

        now = timezone.now()

        if date_filter == 'today':
            start_date = now - timedelta(days=1)

        elif date_filter == 'week':
            start_date = now - timedelta(days=7)

        elif date_filter == 'month':
            start_date = now - timedelta(days=30)

        else:
            start_date = None

        if start_date:
            images = images.filter(
                uploaded_at__gte=start_date
            )

    # Sorting
    if sort == 'oldest':
        images = images.order_by(
            'uploaded_at'
        )

    elif sort == 'name':
        images = images.order_by(
            'original_filename'
        )

    elif sort == 'size':
        images = images.order_by(
            '-compressed_size'
        )

    else:
        images = images.order_by(
            '-uploaded_at'
        )

    return render(
        request,
        'uploads/gallery.html',
        {
            'images': images,
            'search': search,
            'file_type': file_type,
            'date_filter': date_filter,
            'sort': sort,
        }
    )

# ⚡ Infinite Scroll API
@login_required
def gallery_data(request):
    page = request.GET.get('page', 1)
    images = UploadedImage.objects.filter(user=request.user).order_by('-uploaded_at')

    paginator = Paginator(images, 6)
    page_obj = paginator.get_page(page)

    data = []
    for img in page_obj:
        data.append({
            'url': img.image.url,
            'id': img.id
        })

    return JsonResponse(data, safe=False)


# 🗑️ Delete Image (only user's own image)
@login_required
def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id, user=request.user)

    # delete file from media
    if image.image:
        image.image.delete(save=False)

    image.delete()
    return redirect('gallery')

@login_required
def dashboard(request):

    user_images = UploadedImage.objects.filter(
        user=request.user
    )

    total_images = user_images.count()

    total_storage = (
        user_images.aggregate(
            total=Sum('compressed_size')
        )['total'] or 0
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

    recent_images = user_images.order_by(
        '-uploaded_at'
    )[:5]

    return render(
        request,
        'uploads/dashboard.html',
        {
            'total_images': total_images,
            'total_storage': total_storage,
            'monthly_uploads': monthly_uploads,
            'recent_images': recent_images,
        }
    )

@staff_member_required
def admin_dashboard(request):

    total_users = User.objects.count()

    total_images = UploadedImage.objects.count()

    total_storage = (
        UploadedImage.objects.aggregate(
            total=Sum('compressed_size')
        )['total'] or 0
    )

    today = timezone.now().date()

    images_today = UploadedImage.objects.filter(
        uploaded_at__date=today
    ).count()

    recent_users = User.objects.order_by(
        '-date_joined'
    )[:10]

    recent_images = UploadedImage.objects.select_related(
        'user'
    ).order_by(
        '-uploaded_at'
    )[:10]

    return render(
        request,
        'uploads/admin_dashboard.html',
        {
            'total_users': total_users,
            'total_images': total_images,
            'total_storage': total_storage,
            'images_today': images_today,
            'recent_users': recent_users,
            'recent_images': recent_images,
        }
    )