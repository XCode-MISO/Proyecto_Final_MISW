terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.34.0"
    }
  }
}

provider "google" {
  project = "misw-4301-native-cloud-433702"
}

resource "google_pubsub_topic" "pedido_creado" {
  name = "PedidoCreado"
}

resource "google_pubsub_topic" "pedido_despachado" {
  name = "PedidoDespachado"
}

resource "google_pubsub_subscription" "pedido_creado" {
  name = "logistica"
  topic = google_pubsub_topic.pedido_creado.name
}
