resource "aws_apigatewayv2_api" "api" {

  name = var.api_name

  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "integration" {

  api_id = aws_apigatewayv2_api.api.id

  integration_type = "AWS_PROXY"

  integration_uri = var.lambda_invoke_arn

  integration_method = "POST"

  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "root" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.integration.id}"
}

resource "aws_apigatewayv2_route" "proxy" {

  api_id = aws_apigatewayv2_api.api.id

  route_key = "ANY /{proxy+}"

  target = "integrations/${aws_apigatewayv2_integration.integration.id}"
}

resource "aws_apigatewayv2_stage" "stage" {

  api_id = aws_apigatewayv2_api.api.id

  name = "$default"

  auto_deploy = true
}

resource "aws_lambda_permission" "permission" {

  statement_id = "AllowAPIGatewayInvoke"

  action = "lambda:InvokeFunction"

  function_name = var.lambda_invoke_arn

  principal = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.api.execution_arn}/*/*/*"
}
