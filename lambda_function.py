import os

# Set Django settings
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "upload_image_project.settings"
)

import django

# Initialize Django
django.setup()

from django.contrib.auth import get_user_model
from mangum import Mangum
from upload_image_project.asgi import application #Change to wsgi if needed or if any error occurs


# ============================================================
# CREATE DJANGO SUPERUSER IF IT DOES NOT ALREADY EXIST
# ============================================================

User = get_user_model()

ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "himakar@gmail.com"
ADMIN_PASSWORD = "Suchi@98"


# ============================================================
# CREATE ADMIN USER ONLY WHEN ENABLED
# ============================================================

# Create admin only if it doesn't exist
if not User.objects.filter(username=ADMIN_USERNAME).exists():

    User.objects.create_superuser(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD
    )

    print(f"Superuser '{ADMIN_USERNAME}' created successfully.")

else:
    print(f"Superuser '{ADMIN_USERNAME}' already exists.")



# ============================================================
# NORMAL DJANGO APPLICATION HANDLER
# ============================================================
handler = Mangum(application, lifespan='off')