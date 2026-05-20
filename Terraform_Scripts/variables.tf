# AWS

variable "aws_region" {

  default = "us-east-1"
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

  default = "lambda_function.handler"
}

variable "lambda_zip_path" {

  default = "dummy.zip"
}

# DATABASE

variable "db_username" {}

variable "db_password" {

  sensitive = true
}