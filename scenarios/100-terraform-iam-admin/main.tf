# scenarios/100-terraform-iam-admin
# CICD-SEC-2 (Inadequate IAM) — Terraform — CRITICAL
#
# Pattern: an IAM policy granting Action "*" on Resource "*" (full admin). When
# a pipeline applies this and attaches it to its build/deploy role, any
# compromise of the pipeline becomes full cloud-account compromise.
#
# SAFETY: static fixture nested under scenarios/; never `terraform apply`-ed.
# See README.md.

resource "aws_iam_policy" "ci" {
  name = "ci-pipeline"
  # DANGER — wildcard action + resource = full admin. Scope to specific
  # actions/resources (least privilege) instead.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}
