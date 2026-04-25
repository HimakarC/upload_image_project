from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
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
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.user = request.user
            img.save()
            return redirect('success')
    else:
        form = ImageUploadForm()

    return render(request, 'uploads/upload.html', {'form': form})


# ✅ Success Page
@login_required
def success(request):
    return render(request, 'uploads/success.html')


# 🖼️ Gallery Page
@login_required
def gallery(request):
    images = UploadedImage.objects.filter(user=request.user).order_by('-uploaded_at')[:6]
    return render(request, 'uploads/gallery.html', {'images': images})


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
    if image.image and os.path.isfile(image.image.path):
        os.remove(image.image.path)

    image.delete()
    return redirect('gallery')