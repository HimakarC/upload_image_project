# =========================================
# LAMBDA IAM ROLE
# =========================================

resource "aws_iam_role" "lambda_role" {
  name = "${var.lambda_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "lambda.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_s3_policy" {
  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject"
        ]

        Resource = "arn:aws:s3:::${var.bucket_name}/*"
      },
      {
        Effect = "Allow"

        Action = [
          "s3:ListBucket"
        ]

        Resource = "arn:aws:s3:::${var.bucket_name}"
      }
    ]
  })
}


# =========================================
# BASIC LAMBDA EXECUTION POLICY
# =========================================

resource "aws_iam_role_policy_attachment" "lambda_basic" {
role       = aws_iam_role.lambda_role.name
policy_arn = aws_iam_policy.lambda_s3_policy.arn
}

# =========================================
# BASIC LAMBDA FUNCTION
# =========================================

resource "aws_lambda_function" "lambda" {
  function_name = var.lambda_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.handler"
  runtime       = var.lambda_runtime
  timeout       = 30

  filename         = var.lambda_zip_path
  source_code_hash = filebase64sha256(var.lambda_zip_path)

  publish = true

  environment {
    variables = var.environment_variables
  }
}


resource "aws_lambda_alias" "prod" {

  name = "prod"

  function_name = aws_lambda_function.lambda.function_name

  function_version = aws_lambda_function.lambda.version
}