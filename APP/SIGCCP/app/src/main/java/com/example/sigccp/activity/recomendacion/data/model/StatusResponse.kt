package com.example.sigccp.activity.recomendacion.data.model

data class StatusResponse(
    val final_recommendation: String,
    val final_state: String,
    val identified_objects: Array<String>,
    val job_id: String
)
