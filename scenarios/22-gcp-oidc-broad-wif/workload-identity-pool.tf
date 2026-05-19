// DELIBERATELY VULNERABLE — see scenarios/22-gcp-oidc-broad-wif/README.md
//
// This Workload Identity Pool provider lets every repository in the
// greylag-ci org impersonate the production deployer service account.
// Any org member who can create a new repo can mint a production token.

resource "google_iam_workload_identity_pool" "overly_broad" {
  project                   = "example-project"
  workload_identity_pool_id = "overly-broad"
  display_name              = "Overly broad GHA pool"
  description               = "DO NOT REPLICATE — scoped to the entire greylag-ci org."
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = "example-project"
  workload_identity_pool_id          = google_iam_workload_identity_pool.overly_broad.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  // DANGER: matches every repo under greylag-ci/, including any
  // repo that any org member creates in the future.  Should pin to
  // a single repo + environment / branch.
  attribute_condition = "attribute.repository.startsWith('greylag-ci/')"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account_iam_binding" "deployer_impersonation" {
  service_account_id = "projects/example-project/serviceAccounts/example-prod-deployer@example.iam.gserviceaccount.com"
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.overly_broad.name}/attribute.repository/greylag-ci",
  ]
}
