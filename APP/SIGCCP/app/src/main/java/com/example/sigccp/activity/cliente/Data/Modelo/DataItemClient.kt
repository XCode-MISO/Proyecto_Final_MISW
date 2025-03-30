package com.example.sigccp.activity.cliente.Data.Modelo

import androidx.room.PrimaryKey

data class DataItemClient(
    @PrimaryKey
    val id:String ="",
    val name:String ="",
    /*val direction:String ="",
    val location:String ="",
    val email:String="",
    val phone:String ="",
    val dateVisit:String ="",*/
)
