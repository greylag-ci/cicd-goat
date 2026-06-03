# scenarios/119-terraform-s3-unencrypted
# CICD-SEC-7 (Insecure System Configuration) — Terraform
# An S3 bucket with no server-side encryption and no versioning: objects are
# stored unencrypted and can't be recovered after overwrite/delete.
resource "aws_s3_bucket" "artifacts" {
  bucket = "build-artifacts-bucket"
  # DANGER — no aws_s3_bucket_server_side_encryption_configuration and no
  # aws_s3_bucket_versioning reference this bucket: unencrypted, unversioned.
}
