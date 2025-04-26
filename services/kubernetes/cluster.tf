provider "google" {
  project = "misw-4301-native-cloud-433702"
}

resource "google_container_cluster" "microservices-proyecto" {
  name               = "microservices-proyecto"
  location           = "us-central1-c"
  enable_autopilot = true
}


