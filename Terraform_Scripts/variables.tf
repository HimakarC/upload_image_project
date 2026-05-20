variable "aws_region" {}

variable "project_name" {}

variable "environment" {}

# Lambda
variable "lambda_zip_path" {}
variable "lambda_handler" {}
variable "lambda_runtime" {}

# RDS
variable "db_username" {}

variable "db_password" {
  sensitive = true
}

variable "subnet_ids" {
  type = list(string)
}

variable "vpc_id" {}