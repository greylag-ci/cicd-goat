# scenarios/102-terraform-s3-public
# CICD-SEC-7 (Insecure System Configuration) · CICD-SEC-6 — Terraform
#
# Pattern: an S3 bucket whose public-access-block disables every protection, so
# bucket/object ACLs and policies can make it world-readable/writable. A
# pipeline that applies this can expose build artifacts / state / logs publicly.
#
# SAFETY: static fixture nested under scenarios/; never `terraform apply`-ed.
# See README.md.

resource "aws_s3_bucket" "data" {
  bucket = "ci-goat-artifacts"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id
  # DANGER — all four guards disabled; the bucket can be made public. Set every
  # one of these to `true`.
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
