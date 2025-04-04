package com.example.sigccp.activity.pedido.Data.Network

import com.example.sigccp.activity.pedido.Data.Modelo.DataItemPedido
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import javax.inject.Inject

class PedidosService @Inject constructor(
    private val pedidoListClient: ApiServicePedido,
)
{
    fun getPedidosFlow():Flow<List<DataItemPedido>> = flow {
        try {
            val response = pedidoListClient.getPedidos()
            emit(response)
        }
        catch (e: Exception)
        {
            //Manejar exepciones aqui
        }
    }

    fun getPedidoFlow(pedidoId:String):Flow<DataItemPedido> = flow{
        try {
            val response = pedidoListClient.getPedidoId(pedidoId)
            emit(response)
        }
        catch (e: Exception)
        {
            //Manejar exepciones aqui
        }
    }
}