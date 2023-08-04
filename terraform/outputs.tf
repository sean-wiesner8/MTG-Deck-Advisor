output "aws_region" {
  value = "us-west-2"
}

output "s3-bucket" {
  value = aws_s3_bucket.mtg-bucket.id
}
