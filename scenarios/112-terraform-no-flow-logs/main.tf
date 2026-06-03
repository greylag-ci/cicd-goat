# scenarios/112-terraform-no-flow-logs
# CICD-SEC-10 (Insufficient Logging & Visibility) — Terraform
# A VPC with no flow logs and an S3 bucket with no access logging: network
# traffic and bucket access leave no record, so an intrusion is invisible.
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  # DANGER — no aws_flow_log references this VPC: no network visibility.
}

resource "aws_s3_bucket" "data" {
  bucket = "app-data-bucket"
  # DANGER — no access logging configured for this bucket.
}
