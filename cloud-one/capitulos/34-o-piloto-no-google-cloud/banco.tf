resource "google_sql_database_instance" "arraia" {
  name                = "arraia-db"
  database_version    = "POSTGRES_16"
  region              = "southamerica-east1"
  deletion_protection = true

  settings {
    tier              = "db-custom-2-7680"
    availability_type = "REGIONAL"
    disk_autoresize   = true
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.arraia.id
    }
    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "04:00"
    }
    maintenance_window {
      day  = 3
      hour = 5
    }
  }
}
