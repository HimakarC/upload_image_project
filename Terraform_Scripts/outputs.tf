output "api_url" {
  value = module.apigateway.api_url
}

output "database_endpoint" {
  value = module.rds.db_endpoint
}
