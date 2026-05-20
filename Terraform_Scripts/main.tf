provider "aws" {
  region = "us-east-1"
}

module "network" {

  source = "./modules/network"
}

# s3.tf
resource "aws_s3_bucket" "django_media" {
  bucket = "himakarbhavana-${var.environment}"   # Make it unique

  tags = {
    Name        = "Django Media Bucket"
    Environment = var.environment
  }
}

# Block public access (recommended)
resource "aws_s3_bucket_public_access_block" "django_media" {
  bucket = aws_s3_bucket.django_media.id

  block_public_acls       = true   # Set to true if you want fully private
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

module "lambda" {
  source = "./modules/lambda"

  lambda_name     = "django-upload-app"
  lambda_runtime  = "python3.11"
  lambda_handler  = "lambda_function.lambda_handler"
  lambda_zip_path = "./modules/lambda/dummy.zip"
  environment_variables = {
    DJANGO_SETTINGS_MODULE  = "upload_image_project.settings"
    AWS_STORAGE_BUCKET_NAME = aws_s3_bucket.django_media.bucket
    AWS_S3_REGION_NAME      = "us-east-1"

    # === RDS Details ===
    DB_HOST     = module.rds.db_endpoint
    DB_NAME     = module.rds.db_name
    DB_USER     = "postgres"
    DB_PASSWORD = var.db_password
    DB_PORT     = "5432"
  }
}

module "codebuild" {
  source = "./modules/codebuild"

  codebuild_name = "django-codebuild"

  environment_variables = {
    AWS_STORAGE_BUCKET_NAME = aws_s3_bucket.django_media.bucket
    AWS_S3_REGION_NAME      = "us-east-1"

    # === RDS Details ===
    DB_HOST     = module.rds.db_endpoint
    DB_NAME     = module.rds.db_name
    DB_USER     = "postgres"
    DB_PASSWORD = var.db_password
    DB_PORT     = "5432"
  }

}

module "codepipeline" {
  source = "./modules/codepipeline"

  pipeline_name = "${var.project_name}"

  bucket_name = "dev-django-pipeline-bucket"

  codebuild_project_name = module.codebuild.project_name
  lambda_function_name   = module.lambda.lambda_name
}

module "apigateway" {

  source = "./modules/apigateway"

  api_name = "${var.environment}-${var.project_name}-api"

  lambda_invoke_arn = module.lambda.lambda_invoke_arn

  lambda_name = module.lambda.lambda_name
}

module "rds" {

  source = "./modules/rds"

  rds_name = "${var.environment}-${var.project_name}-db"

  db_username = var.db_username

  db_password = var.db_password

  subnet_ids = module.network.subnet_ids

  vpc_id = module.network.vpc_id
}