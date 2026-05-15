# Django Image Upload Web Application

A full-stack Django-based Image Upload Web Application integrated with AWS services including AWS Lambda, API Gateway, Amazon RDS PostgreSQL, CodeBuild, and CodePipeline.

---

# Features

- User Registration & Login Authentication
- Secure Image Upload Functionality
- Dynamic Image Gallery
- PostgreSQL Database Integration
- AWS Lambda Deployment
- API Gateway Integration
- CI/CD Pipeline using AWS CodeBuild & CodePipeline

---

# Technologies Used

- Django
- AWS Lambda
- AWS API Gateway
- AWS CodeBuild
- AWS CodePipeline
- Amazon RDS

---

# Phase-I : Django Project Development

## Step-1 : Create Virtual Environment

### Create Virtual Environment

```bash
python3 -m venv env
```

### Activate Virtual Environment (CMD)

```bash
env\Scripts\activate.bat
```

### Activate Virtual Environment (PowerShell)

```bash
env/Scripts/Activate.ps1
```

### Install Django

```bash
pip install django
```

---

## Step-2 : Create Django Project

```bash
django-admin startproject upload_image_project
```

Move into project directory:

```bash
cd upload_image_project
```

---

## Step-3 : Create Django Application

```bash
python manage.py startapp uploads
```

---

## Step-4 : Create HTML Templates

Create the following directory structure:

```bash
uploads/templates/uploads/
```

Create the following HTML files:

- base.html
- gallery.html
- login.html
- register.html
- success.html
- upload.html

---

## Step-5 : Create Django Associated Files

Configure the following files:

- urls.py
- views.py
- forms.py
- models.py

### Purpose of Each File

| File | Purpose |
|------|----------|
| models.py | Database integration |
| urls.py | URL routing |
| views.py | Business logic |
| forms.py | Form handling for image uploads |


---

# Project Structure

```bash
upload_image_project/
│
├── upload_image_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
├── uploads/
│   ├── migrations/
│   │   └── __init__.py
│   │
│   ├── templates/
│   │   └── uploads/
│   │       ├── success.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── upload.html
│   │       ├── gallery.html
│   │       └── base.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
└── requirements.txt
```

---

# Phase-II : Database Integration

## Step-1 : Create Amazon RDS PostgreSQL Database

- Open AWS Console
- Search for RDS
- Create PostgreSQL Database Instance
- Configure:
  - DB Instance Identifier
  - Username
  - Password

---

## Step-2 : Connect Database using PGAdmin

Use the RDS Endpoint to connect PostgreSQL database with PGAdmin.

---

## Step-3 : Configure Database in Django

Add PostgreSQL configuration in:

```python
settings.py
```

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database_name',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'rds-endpoint',
        'PORT': '5432',
    }
}
```

---

## Step-4 : Apply Database Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

# Phase-III : AWS Lambda Integration

## Step-1 : Create lambda_function.py

Create file:

```bash
lambda_function.py
```

Example Code:

```python
import os
from django.core.wsgi import get_wsgi_application
from mangum import Mangum

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upload_image_project.settings')

application = get_wsgi_application()

handler = Mangum(application)
```

---

## Step-2 : Create AWS Lambda Function

- Open AWS Lambda
- Create Function
- Runtime: Python
- Architecture: x86_64

---

## Step-3 : Configure Lambda Function

### Change Handler

```bash
lambda_function.handler
```

### Increase Timeout

```bash
30 seconds
```

---

# Phase-IV : CodeBuild Integration

## Step-1 : Create buildspec.yml

Create file:

```bash
buildspec.yml
```

Example:

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.12

    commands:
      - pip install -r requirements.txt -t .

artifacts:
  files:
    - '**/*'
```

---

## Step-2 : Create CodeBuild Project

- Open AWS CodeBuild
- Create Build Project
- Source Provider: GitHub
- Repository: Select Your Repository
- Buildspec: Use buildspec.yml

---

# Phase-V : CodePipeline Integration

## Step-1 : Create CodePipeline

- Open AWS CodePipeline
- Create Pipeline

---

## Step-2 : Configure Source Stage

- Source Provider:
  - GitHub
  - CodeCommit
  - S3

Select:
- Repository
- Branch

---

## Step-3 : Configure Build Stage

- Build Provider: AWS CodeBuild
- Select Existing Build Project

---

## Step-4 : Configure Deploy Stage

- Deploy Provider: AWS Lambda
- Select Lambda Function

---

# Phase-VI : API Gateway Integration

## Step-1 : Create HTTP API

- Open AWS API Gateway
- Select HTTP API
- Create API

---

## Step-2 : Create Routes

Create Route:

```bash
ANY /prod
```

or

```bash
ANY /dev
```

---

## Step-3 : Attach Lambda Integration

- Open Integrations and Routes
- Attach Lambda Function

---

## Step-4 : Deploy API

Create Stage:
- $default
- dev
- prod
- test

---

# Important Phase : Serverless Django Integration

## Step-1 : Modify settings.py

Add:

```python
USE_X_FORWARDED_HOST = True
```

---

## Step-2 : Configure Proxy Routing in API Gateway

Create Route:

```bash
ANY /{proxy+}
```

Attach Lambda Integration and Deploy to:

```bash
$default
```

---

## Step-3 : Add API Gateway Trigger in Lambda

- Open Lambda Function
- Add Trigger
- Select API Gateway
- Attach Existing API

---

# Final Project Structure

```bash
upload_image_project/
│
├── upload_image_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
├── uploads/
│   ├── migrations/
│   │   └── __init__.py
│   │
│   ├── templates/
│   │   └── uploads/
│   │       ├── success.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── upload.html
│   │       ├── gallery.html
│   │       └── base.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── buildspec.yml
├── lambda_function.py
└── requirements.txt
```

---

# Deployment Workflow

```text
GitHub
   ↓
CodePipeline
   ↓
CodeBuild
   ↓
AWS Lambda
   ↓
API Gateway
   ↓
Django Application
```

---

# Important Notes

- Ensure proper `buildspec.yml` configuration
- Avoid nested folders inside deployment ZIP
- Use compatible Python runtime versions
- Configure API Gateway proxy routes correctly
- Ensure Lambda handler is properly configured
