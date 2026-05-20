variable "codebuild_name" {}

variable "s3_media_bucket_name" {
  description = "Name of the S3 bucket for Django media files"
  type        = string
}