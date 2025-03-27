
resource "google_pubsub_topic" "pedido_creado" {
  name = "PedidoCreado"
}

resource "google_pubsub_subscription" "logistica" {
  name  = "logistica"
  topic = google_pubsub_topic.pedido_creado.name
}
