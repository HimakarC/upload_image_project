variable "lambda_name" {}

variable "lambda_zip_path" {}

variable "lambda_handler" {}

variable "lambda_runtime" {}

variable "environment_variables" {
  description = "Environment variables for Lambda"
  type        = map(string)
  default     = {}
}