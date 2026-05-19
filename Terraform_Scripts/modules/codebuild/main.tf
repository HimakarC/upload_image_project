resource "aws_iam_role" "codebuild_role" {

  name = "${var.codebuild_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "codebuild.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "admin" {

  role = aws_iam_role.codebuild_role.name

  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_codebuild_project" "project" {

  name = var.codebuild_name

  service_role = aws_iam_role.codebuild_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {

    compute_type = "BUILD_GENERAL1_SMALL"

    image = "aws/codebuild/standard:7.0"

    type = "LINUX_CONTAINER"
  }

  source {

    type = "GITHUB"

    location = "https://github.com/${var.github_owner}/${var.github_repo}.git"

    buildspec = "buildspec.yml"
  }
}
