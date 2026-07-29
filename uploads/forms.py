from django import forms
from PIL import Image, UnidentifiedImageError

from .models import UploadedImage


class ImageUploadForm(forms.ModelForm):

    class Meta:

        model = UploadedImage

        fields = [
            "image"
        ]

    def clean_image(self):

        image_file = self.cleaned_data.get(
            "image"
        )

        if not image_file:
            raise forms.ValidationError(
                "Please select an image."
            )

        # Maximum size = 10 MB
        max_size = 10 * 1024 * 1024

        if image_file.size > max_size:

            raise forms.ValidationError(
                "Image size must not exceed 10 MB."
            )

        # Allowed extensions
        allowed_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        ]

        filename = image_file.name.lower()

        if not any(
            filename.endswith(extension)
            for extension in allowed_extensions
        ):

            raise forms.ValidationError(
                "Only JPG, JPEG, PNG and WEBP "
                "images are allowed."
            )

        try:

            image = Image.open(
                image_file
            )

            # Verify actual image
            image.verify()

            # Re-open after verify
            image_file.seek(0)

            image = Image.open(
                image_file
            )

            width, height = image.size

            # Minimum dimensions
            if width < 100 or height < 100:

                raise forms.ValidationError(
                    "Image dimensions must be at least "
                    "100 x 100 pixels."
                )

        except UnidentifiedImageError:

            raise forms.ValidationError(
                "The uploaded file is not a valid image."
            )

        except forms.ValidationError:

            raise

        except Exception:

            raise forms.ValidationError(
                "The image appears to be corrupted "
                "or invalid."
            )

        image_file.seek(0)

        return image_file