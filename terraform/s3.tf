resource "aws_s3_bucket" "mtg-bucket" {
  bucket_prefix = "sean-wiesner-mtg-project"
  force_destroy = true
}
