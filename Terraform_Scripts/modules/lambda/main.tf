resource "aws_iam_role" "lambda_role" {

  name = "${var.lambda_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "lambda.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "basic" {

  role = aws_iam_role.lambda_role.name

  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "lambda" {

  function_name = var.lambda_name

  role = aws_iam_role.lambda_role.arn

  runtime = var.lambda_runtime

  handler = var.lambda_handler

  filename = var.lambda_zip_path

  source_code_hash = filebase64sha256(var.lambda_zip_path)

  timeout = 30
}
