output "api_url" {
  value = module.apigateway.api_url
}

output "database_endpoint" {
  value = module.rds.db_endpoint
}

output "s3_media_bucket_name" {
  value = aws_s3_bucket.django_media.bucket
}