package com.example.sigccp.activity.recomendacion.data.model

data class StatusResponse(
    val final_recommendation: String,
    val final_state: String,
    val identified_objects: Array<String>,
    val job_id: String,
    val recommended_products: List<Producto>
)

data class Producto(
    val nombre: String,
    val precio: Double,
    val producto_id: Int,
    val stock: Int
)