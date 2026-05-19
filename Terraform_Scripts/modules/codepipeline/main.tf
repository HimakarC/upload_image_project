resource "aws_s3_bucket" "bucket" {

  bucket = var.bucket_name
}

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

resource "aws_iam_role_policy_attachment" "admin" {

  role = aws_iam_role.pipeline_role.name

  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_codepipeline" "pipeline" {

  name = var.pipeline_name

  role_arn = aws_iam_role.pipeline_role.arn

  artifact_store {

    location = aws_s3_bucket.bucket.bucket

    type = "S3"
  }

  stage {

    name = "Source"

    action {

      name = "Source"

      category = "Source"

      owner = "ThirdParty"

      provider = "GitHub"

      version = "1"

      output_artifacts = ["source_output"]

      configuration = {

        Owner = var.github_owner

        Repo = var.github_repo

        Branch = var.github_branch

        OAuthToken = var.github_token
      }
    }
  }

  stage {

    name = "Build"

    action {

      name = "Build"

      category = "Build"

      owner = "AWS"

      provider = "CodeBuild"

      input_artifacts = ["source_output"]

      output_artifacts = ["build_output"]

      version = "1"

      configuration = {
        ProjectName = var.codebuild_project_name
      }
    }
  }
}
