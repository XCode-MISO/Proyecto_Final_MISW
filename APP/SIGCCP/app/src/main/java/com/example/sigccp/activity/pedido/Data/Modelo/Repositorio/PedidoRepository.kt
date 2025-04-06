package com.example.sigccp.activity.pedido.Data.Modelo.Repositorio

import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import com.example.sigccp.activity.pedido.Data.Network.PedidoService
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import javax.inject.Inject

class PedidoRepository @Inject constructor(private val api: PedidoService) {

    fun getPedidosFlow(): Flow<List<PedidoClass>> = flow {
        val pedidos = api.obtenerPedidos()
        emit(pedidos)
    }

    fun getPedidoFlow(pedidoId: String): Flow<PedidoClass> = flow {
        val pedido = api.obtenerPedidos().find { it.id == pedidoId }
        if (pedido != null) {
            emit(pedido)
        }
    }
}
