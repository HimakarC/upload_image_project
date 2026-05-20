provider "aws" {
  region = "us-east-1"
}

module "network" {

  source = "./modules/network"
}

resource "aws_lambda_function" "lambda" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  handler       = var.handler
  runtime       = var.runtime
  timeout       = 30

  # Dummy ZIP only for Terraform creation
  filename         = "${path.module}/dummy.zip"
  source_code_hash = filebase64sha256("${path.module}/dummy.zip")

  lifecycle {
    ignore_changes = [
      filename,
      source_code_hash,
      last_modified,
    ]
  }

  environment {
    variables = {
      DJANGO_SETTINGS_MODULE = "upload_image_project.settings"
    }
  }
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

module "codebuild" {

  source = "./modules/codebuild"

  codebuild_name = "${var.environment}-${var.project_name}-build"
}

module "codepipeline" {

  source = "./modules/codepipeline"

  pipeline_name = "${var.environment}-${var.project_name}-pipeline"

  bucket_name = "${var.environment}-${var.project_name}-bucket"

  codebuild_project_name = module.codebuild.project_name
}