resource "aws_s3_bucket" "mtg-bucket" {
  bucket_prefix = "mtg-project"
  force_destroy = true
}
