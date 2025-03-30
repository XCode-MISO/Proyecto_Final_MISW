package com.example.sigccp.activity.producto.Data.Modelo

import androidx.room.PrimaryKey

data class DataItemProducto(
    @PrimaryKey
    val id:String ="",
    val name:String ="",/*
    val price: Float =0.0f,
    val amount:Int=0,*/
)
