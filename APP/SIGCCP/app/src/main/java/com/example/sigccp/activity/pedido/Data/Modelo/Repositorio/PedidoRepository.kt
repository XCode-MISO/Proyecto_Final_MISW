package com.example.sigccp.activity.pedido.Data.Modelo.Repositorio

import com.example.sigccp.activity.pedido.Data.Modelo.DataItemPedido
import com.example.sigccp.activity.pedido.Data.Network.PedidosService
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

class PedidoRepository  @Inject constructor(private val api: PedidosService)
{
    fun getPedidosFlow(): Flow<List<DataItemPedido>> = api.getPedidosFlow()

    fun getPedidoFlow(pedidoId:String): Flow<DataItemPedido> = api.getPedidoFlow(pedidoId)

}