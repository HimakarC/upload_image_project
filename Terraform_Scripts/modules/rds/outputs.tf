output "db_endpoint" {
  value = aws_db_instance.postgres.address
}

output "db_name" {
  value = var.db_name
}