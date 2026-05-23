# =========================================
# S3 BUCKET FOR PIPELINE ARTIFACTS
# =========================================

resource "aws_s3_bucket" "pipeline_bucket" {

  bucket = var.bucket_name
}

# =========================================
# IAM ROLE FOR CODEPIPELINE
# =========================================

resource "aws_iam_role" "pipeline_role" {

  name = "${var.pipeline_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "codepipeline.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })
}

# =========================================
# IAM POLICY ATTACHMENT
# =========================================

resource "aws_iam_role_policy_attachment" "pipeline_policy" {

  role = aws_iam_role.pipeline_role.name

  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

# =========================================
# CODEPIPELINE
# =========================================

resource "aws_codepipeline" "pipeline" {

  name = var.pipeline_name

  role_arn = aws_iam_role.pipeline_role.arn

  artifact_store {

    location = aws_s3_bucket.pipeline_bucket.bucket

    type = "S3"
  }

  # ======================================
  # SOURCE STAGE
  # ======================================

  stage {
    name = "Source"
    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["source_output"]
      configuration = {
        ConnectionArn    = "arn:aws:codeconnections:us-east-1:566057504080:connection/21d7d256-153b-4a86-bdda-210d6dc65e88"
        FullRepositoryId = "HimakarC/upload_image_project"
        BranchName       = "dev"
      }
      run_order = 1
    }
  }

  # ======================================
  # BUILD STAGE
  # ======================================
  
  stage {

    name = "Build"

    action {

      name = "CodeBuild"

      category = "Build"

      owner = "AWS"

      provider = "CodeBuild"

      version = "1"

      input_artifacts = ["source_output"]

      output_artifacts = ["build_output"]

      configuration = {

        ProjectName = var.codebuild_project_name
      }

      run_order = 1
    }
  }

  # ======================================
  # BUILD DEPLOY
  # ======================================
  
  stage {
    name = "Deploy"

    action {
      name            = "LambdaDeploy"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "Lambda"
      input_artifacts = ["build_output"]
      version         = "1"

      configuration = {
        FunctionName = var.lambda_function_name
      }
    }
  }
}
