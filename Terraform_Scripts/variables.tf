# AWS

variable "aws_region" {

  default = "ap-south-1"
}

# =========================================
# PROJECT
# =========================================

variable "project_name" {}

variable "environment" {

  default = "dev"
}


# Lambda

variable "lambda_runtime" {

  default = "python3.11"
}

variable "lambda_handler" {

  default = "lambda_function.lambda_handler"
}

variable "lambda_zip_path" {

  default = "django_lambda.zip"
}


# DATABASE

variable "db_username" {}

variable "db_password" {

  sensitive = true
}