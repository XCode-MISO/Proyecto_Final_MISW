package com.example.sigccp.activity.entrega.ui.view

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
import com.example.sigccp.R
import com.example.sigccp.activity.entrega.data.model.Entrega
import com.example.sigccp.activity.entrega.ui.viewmodel.ListarEntregasViewModel
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.ui.View.Components.locationDropdown
import com.example.sigccp.ui.View.Components.moneda
import com.example.sigccp.ui.theme.AmarilloApp
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.MoradoApp

@Composable
fun ListarEntregas(viewModel: ListarEntregasViewModel = viewModel()) {
    val clientId = PreferencesManager.getString(PreferenceKeys.USER_ID)
    LaunchedEffect(clientId) {
        viewModel.fetchEntregas(clientId)
    }
    val isLoading = viewModel.isLoading.collectAsState().value
    val entregas = viewModel.entregas.collectAsState().value

    val monedaSeleccionada = remember { mutableStateOf(1) }
    ScreenContainer(title = stringResource(id = R.string.delivery),
        salirenabled = true,
        enabled = false,
        showBackButton = true,
        imagen = null,
        backDestination = AppScreen.Menu.route)
    {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            locationDropdown(
                locations = moneda,
                onLocationtSelected = { nombreMoneda ->
                    monedaSeleccionada.value = nombreMoneda
                }
            )
            Spacer(modifier = Modifier.height(16.dp))

            if (isLoading) {
                CircularProgressIndicator()
            } else {
                ListaDeEntregas(entregas.filter { it.state != "Entregado" }, moneda = monedaSeleccionada.value)
            }
        }
    }
}


@Composable
fun ListaDeEntregas(entregas: List<Entrega>, moneda : Int) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(entregas) { entrega: Entrega  ->
            EntregaBox(entrega, moneda)
        }
    }
}

@Composable
fun EntregaBox(
    entrega: Entrega,
    moneda: Int
) {
    val tasaConversion = 4000f
    val precioConvertido = if (moneda == 2) entrega.price * tasaConversion else entrega.price
    val simbolo = if (moneda == 2) "COP" else "USD"
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(AmarilloApp, shape = RoundedCornerShape(8.dp))
            .border(2.dp, MoradoApp, shape = RoundedCornerShape(8.dp)),
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier.fillMaxWidth(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = entrega.name,
                    style = AppTypography.labelMedium,
                    modifier = Modifier
                        .weight(1f)
                        .padding(4.dp)
                        .align(Alignment.CenterVertically),
                    textAlign = TextAlign.Center
                )

                Text(
                    text = entrega.deliveryDate,
                    style = AppTypography.labelMedium,
                    modifier = Modifier
                        .weight(1f)
                        .padding(4.dp)
                        .align(Alignment.CenterVertically),
                    textAlign = TextAlign.Center
                )
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "Valor: ",
                    style = AppTypography.labelMedium,
                    modifier = Modifier
                        .weight(1f)
                        .padding(4.dp)
                        .align(Alignment.CenterVertically),
                    textAlign = TextAlign.Center
                )
                Text(
                    text = "$${"%.2f".format(precioConvertido)} $simbolo",
                    style = AppTypography.labelMedium,
                    modifier = Modifier
                        .weight(1f)
                        .padding(4.dp)
                        .align(Alignment.CenterVertically),
                    textAlign = TextAlign.Center
                )

            }
        }
    }
}