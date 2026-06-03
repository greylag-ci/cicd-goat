# scenarios/101-terraform-sg-open
# CICD-SEC-7 (Insecure System Configuration) — Terraform — CRITICAL
#
# Pattern: a security group opens SSH (port 22) to the whole internet
# (`0.0.0.0/0`). Applied by a pipeline, it exposes the instance to the world.
#
# SAFETY: static fixture nested under scenarios/; never `terraform apply`-ed.
# See README.md.

resource "aws_security_group" "ci" {
  name = "ci-runner"
  ingress {
    description = "ssh"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    # DANGER — SSH open to the entire internet. Restrict to known CIDRs.
    cidr_blocks = ["0.0.0.0/0"]
  }
}
