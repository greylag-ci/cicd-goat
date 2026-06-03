# scenarios/120-terraform-rds-public
# CICD-SEC-7 (Insecure System Configuration) · CICD-SEC-2 — Terraform
# An RDS instance reachable from the internet with encryption-at-rest off.
variable "db_password" {
  type      = string
  sensitive = true
}

resource "aws_db_instance" "main" {
  engine            = "postgres"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  username          = "admin"
  password          = var.db_password
  # DANGER — internet-reachable database with unencrypted storage.
  publicly_accessible = true
  storage_encrypted   = false
  skip_final_snapshot = true
}
