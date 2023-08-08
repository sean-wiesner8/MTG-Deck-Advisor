output "aws_region" {
  value = "us-west-2"
}

output "s3_bucket" {
  value = aws_s3_bucket.mtg-bucket.id
}

output "rds_database_name" {
  description = "Database name in the RDS cluster"
  value       = aws_db_instance.mtg_db.db_name
}

output "rds_hostname" {
  description = "RDS instance hostname"
  value       = aws_db_instance.mtg_db.address
}

output "rds_instance_endpoint" {
  description = "Endpoint of the RDS cluster"
  value       = aws_db_instance.mtg_db.endpoint
}

output "rds_username" {
  description = "Username of the RDS cluster"
  value       = aws_db_instance.mtg_db.username
}

output "rds_password" {
  description = "Password for the RDS cluster"
  value       = var.db_password
}

output "rds_port" {
  description = "Port for the RDS cluster"
  value       = aws_db_instance.mtg_db.port
}
