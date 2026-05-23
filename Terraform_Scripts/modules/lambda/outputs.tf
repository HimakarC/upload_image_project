output "lambda_name" {
  value = aws_lambda_function.lambda.function_name
}

output "lambda_invoke_arn" {
  value = aws_lambda_function.lambda.invoke_arn
}

output "lambda_alias_arn" {
  value = aws_lambda_alias.prod.arn
}