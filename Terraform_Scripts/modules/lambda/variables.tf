variable "lambda_name" {}

variable "lambda_zip_path" {}

variable "lambda_handler" {}

variable "lambda_runtime" {}

variable "s3_media_bucket_name" {
  description = "Name of the S3 bucket for Django media files"
  type        = string
}