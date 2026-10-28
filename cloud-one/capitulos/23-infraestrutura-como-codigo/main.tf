terraform {
  required_providers {
    google = { source = "hashicorp/google" }
  }
}

provider "google" {
  project = var.projeto
  region  = "southamerica-east1"
}

variable "projeto" {
  type = string
}

resource "google_storage_bucket" "originais" {
  name                        = "${var.projeto}-originais"
  location                    = "southamerica-east1"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  versioning { enabled = true }
}

output "bucket_originais" {
  value = google_storage_bucket.originais.url
}
