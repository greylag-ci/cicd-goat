# scenarios/111-terraform-cloudtrail-disabled
# CICD-SEC-10 (Insufficient Logging & Visibility) — Terraform
# A CloudTrail with logging turned off, single-region, no log-file
# validation: the account's API-activity audit trail is effectively blind.
resource "aws_cloudtrail" "main" {
  name           = "org-trail"
  s3_bucket_name = "org-trail-bucket"
  # DANGER — no audit trail: logging off, single-region, validation off.
  enable_logging                = false
  is_multi_region_trail         = false
  include_global_service_events = false
  enable_log_file_validation    = false
}
