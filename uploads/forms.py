from django import forms
from PIL import Image, UnidentifiedImageError
from .models import UploadedImage


class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = UploadedImage
        fields = ['image']

    def clean_image(self):
        image_file = self.cleaned_data.get('image')

        if not image_file:
            raise forms.ValidationError(
                "Please select an image."
            )

        # Maximum size: 10 MB
        max_size = 10 * 1024 * 1024

        if image_file.size > max_size:
            raise forms.ValidationError(
                "Image size must not exceed 10 MB."
            )

        # Allowed extensions
        allowed_extensions = [
            '.jpg',
            '.jpeg',
            '.png',
            '.webp'
        ]

        filename = image_file.name.lower()

        if not any(
            filename.endswith(ext)
            for ext in allowed_extensions
        ):
            raise forms.ValidationError(
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )

        # Verify actual image content
        try:
            img = Image.open(image_file)

            img.verify()

            # Re-open because verify() closes the image
            image_file.seek(0)

            img = Image.open(image_file)

            width, height = img.size

            # Minimum dimensions
            if width < 100 or height < 100:
                raise forms.ValidationError(
                    "Image dimensions must be at least 100x100 pixels."
                )

        except UnidentifiedImageError:
            raise forms.ValidationError(
                "The uploaded file is not a valid image."
            )

        except Exception:
            raise forms.ValidationError(
                "The image appears to be corrupted or invalid."
            )

        image_file.seek(0)

        return image_file