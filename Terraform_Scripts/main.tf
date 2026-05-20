provider "aws" {
  region = "us-east-1"
}

module "network" {

  source = "./modules/network"
}

module "lambda" {
  source = "./modules/lambda"

  function_name = var.lambda_function_name
  runtime        = "python3.11"
  handler        = "lambda_function.handler"
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