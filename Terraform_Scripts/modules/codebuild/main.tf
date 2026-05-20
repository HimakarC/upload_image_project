# =========================================
# IAM ROLE FOR CODEBUILD
# =========================================

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

# =========================================
# IAM POLICY ATTACHMENT
# =========================================

resource "aws_iam_role_policy_attachment" "codebuild_policy" {

  role = aws_iam_role.codebuild_role.name

  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

# =========================================
# CLOUDWATCH LOG GROUP
# =========================================

resource "aws_cloudwatch_log_group" "codebuild_logs" {

  name = "/aws/codebuild/${var.codebuild_name}"
}

# =========================================
# CODEBUILD PROJECT
# =========================================

resource "aws_codebuild_project" "project" {

  name = var.codebuild_name

  service_role = aws_iam_role.codebuild_role.arn

  build_timeout = 30

  artifacts {

    type = "CODEPIPELINE"
  }

  environment {

    compute_type = "BUILD_GENERAL1_SMALL"

    image = "aws/codebuild/standard:7.0"

    type = "LINUX_CONTAINER"

    privileged_mode = true

    dynamic "environment_variable" {
      for_each = var.environment_variables
      content {
        name  = environment_variable.key
        value = environment_variable.value
        type  = "PLAINTEXT"
      }
    }
  }

  source {

    type = "CODEPIPELINE"

    buildspec = "buildspec.yml"
  }

  logs_config {

    cloudwatch_logs {

      group_name = aws_cloudwatch_log_group.codebuild_logs.name

      status = "ENABLED"
    }
  }

  tags = {
    Environment = "dev"
    Project     = var.codebuild_name
  }
}