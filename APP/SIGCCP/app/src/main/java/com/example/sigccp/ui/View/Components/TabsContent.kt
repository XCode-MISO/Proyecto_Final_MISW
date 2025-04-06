package com.example.sigccp.ui.View.Components

import android.app.Activity
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsHoveredAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.compositeOver
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import com.example.sigccp.activity.pedido.Data.Modelo.Pedidos
import com.example.sigccp.activity.producto.Data.Modelo.ProductoClass
import com.example.sigccp.activity.producto.Data.Modelo.ProductosPedidoClass
import com.example.sigccp.ui.theme.AmarilloApp
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.MoradoApp
import com.example.sigccp.ui.theme.RojoApp
import com.example.sigccp.ui.theme.VerdeApp
import com.example.sigccp.utils.getSavedLanguage
import com.example.sigccp.utils.restartActivity
import com.example.sigccp.utils.saveLanguage
import com.example.sigccp.utils.setAppLocale

@Composable
fun newButton(
    onClick: () -> Unit,
    nombre: String,
    buttonWidth: Dp = 200.dp // 🔹 Ancho definido por defecto en 200.dp
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isHovered by interactionSource.collectIsHoveredAsState()
    val buttonColor = AmarilloApp
    val hoverColor = buttonColor.copy(alpha = 1f).compositeOver(Color.Black.copy(alpha = 0.3f))
    val currentColor = if (isHovered) hoverColor else buttonColor

    Box(
        modifier = Modifier
            .width(buttonWidth) // 🔹 Ancho fijo en lugar de fillMaxWidth()
            .border(2.dp, MoradoApp, RoundedCornerShape(12.dp))
    ) {
        // Sombra debajo del botón
        Box(
            modifier = Modifier
                .width(buttonWidth) // 🔹 Ancho fijo
                .height(4.dp)
                .background(Color.Black.copy(alpha = 0.3f))
                .align(Alignment.BottomCenter)
                .clip(RoundedCornerShape(12.dp))
                .offset(y = 2.dp)
        )

        // Fondo del botón
        Box(
            modifier = Modifier
                .width(buttonWidth) // 🔹 Ancho fijo
                .padding(bottom = 4.dp)
                .clip(RoundedCornerShape(12.dp))
                .background(currentColor)
        ) {
            Button(
                onClick = onClick,
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.Transparent // Botón transparente
                ),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .width(buttonWidth) // 🔹 Ancho fijo
                    .semantics { contentDescription = nombre },
                interactionSource = interactionSource
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Start
                ) {
                    Box(
                        modifier = Modifier.fillMaxWidth(),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = nombre,
                            style = AppTypography.labelLarge
                        )
                    }
                }
            }
        }

        if (isHovered) {
            Box(
                modifier = Modifier
                    .width(buttonWidth) // 🔹 Ancho fijo
                    .matchParentSize()
                    .background(Color.Black.copy(alpha = 0.3f))
                    .clip(RoundedCornerShape(12.dp))
            )
        }
    }
}


@Composable
fun newMenuButton(
    onClick: () -> Unit, nombre: String, imagen: Int, enabled: Boolean = true)
{
    val interactionSource = remember { MutableInteractionSource() }
    val isHovered by interactionSource.collectIsHoveredAsState()
    val buttonColor = VerdeApp
    val hoverColor = buttonColor.copy(alpha = 1f).compositeOver(Color.Black.copy(alpha = 0.3f))
    val currentColor = if (isHovered) hoverColor else buttonColor
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .border(2.dp, MoradoApp, RoundedCornerShape(12.dp)) // Borde con el color especificado
    ) {
        // Sombra debajo del botón
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(4.dp) // Altura de la sombra
                .background(Color.Black.copy(alpha = 0.3f)) // Color y opacidad de la sombra
                .align(Alignment.BottomCenter) // Alinear la sombra al fondo
                .clip(RoundedCornerShape(12.dp)) // Redondear las esquinas de la sombra
                .offset(y = 2.dp) // Desplazar hacia abajo
        )

        // Fondo del botón
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 4.dp)
                .clip(RoundedCornerShape(12.dp))
                .background(currentColor)
        ) {
            Button(
                enabled = enabled,
                onClick = onClick,
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.Transparent // Hacer el botón transparente
                ),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .semantics { contentDescription = nombre },
                interactionSource = interactionSource
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Start
                ) {
                    Image(
                        painter = painterResource(id = imagen),
                        contentDescription = nombre,
                        modifier = Modifier
                            .size(30.dp)
                            .padding(end = 3.dp)
                    )
                    Box(
                        modifier = Modifier.fillMaxWidth(),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = nombre,
                            style = AppTypography.labelLarge
                        )
                    }
                }
            }
        }

        if (isHovered) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .matchParentSize() // Cubre todo el botón
                    .background(Color.Black.copy(alpha = 0.3f)) // Oscurecimiento
                    .clip(RoundedCornerShape(12.dp)) // Mantener esquinas redondeadas
            )
        }
    }
}

//SubTitle App
@Composable
fun SubTitleBar( texto:String, imagen:Int? = null, enabled: Boolean = true)  {
    Row(
        verticalAlignment = Alignment.CenterVertically
    )
    {
        Text(
            textAlign = TextAlign.Justify,
            text = texto,
            style = AppTypography.titleSmall
        )
        if (enabled && imagen != null) {
            Box(
                modifier = Modifier.size(40.dp),
                contentAlignment = Alignment.Center,
            ) {
                Image(
                    painter = painterResource(id = imagen),
                    contentDescription = "Imagen asociada",
                    modifier = Modifier
                        .size(40.dp)
                        .padding(end = 3.dp)
                )
            }
        }
    }
}



// DropDown de Lenguaje
@Composable
fun LanguageDropdown(activity: Activity?) {
    var expanded by remember { mutableStateOf(false) }
    val context = LocalContext.current
    var selectedLanguage by remember { mutableStateOf(getSavedLanguage(context).uppercase()) }
    val recomposer = remember { mutableStateOf(0) }

    Box(
        modifier = Modifier.wrapContentSize(Alignment.TopEnd)
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(end = 20.dp)
        ) {
            IconButton(
                onClick = { expanded = true }
            ) {
                Icon(
                    imageVector = Icons.Outlined.Public,
                    contentDescription = "Idioma",
                    tint = MoradoApp,
                    modifier = Modifier.size(40.dp)
                )
            }
            Text(
                text = selectedLanguage,
                color = MoradoApp,
                style = AppTypography.titleSmall
            )
            DropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                DropdownMenuItem(
                    text = { Text("ES", style =AppTypography.titleSmall) },
                    onClick = {
                        selectedLanguage = "ES"
                        setAppLocale(activity, "es")
                        saveLanguage(context, "ES")
                        expanded = false
                        restartActivity(activity)
                        recomposer.value++
                    }
                )
                DropdownMenuItem(
                    text = { Text("EN", style =AppTypography.titleSmall) },
                    onClick = {
                        selectedLanguage = "EN"
                        setAppLocale(activity, "en")
                        saveLanguage(context, "EN")
                        expanded = false
                        restartActivity(activity)
                        recomposer.value++
                    }
                )
            }
        }
    }
}


// DropDown de Cliente
@Composable
fun ClientDropdown(
    clients: List<Pair<Int, String>>, // Lista de clientes (id, name)
    onClientSelected: (Int) -> Unit // Callback con el ID del cliente seleccionado
) {
    var expanded by remember { mutableStateOf(false) }
    var selectedClient by remember { mutableStateOf<Pair<Int, String>?>(null) }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .border(2.dp, MoradoApp, shape = RoundedCornerShape(8.dp))
            .clickable { expanded = true }
            .padding(12.dp),
        contentAlignment = Alignment.CenterStart
    ) {
        Text(
            text = selectedClient?.second ?: "Seleccione un cliente",
            style = AppTypography.labelLarge
        )

        Icon(
            imageVector = Icons.Default.ArrowDropDown,
            contentDescription = "Desplegar",
            modifier = Modifier.align(Alignment.CenterEnd)
        )

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            clients.forEach { client ->
                DropdownMenuItem(
                    text = { Text(client.second) },
                    onClick = {
                        selectedClient = client
                        onClientSelected(client.first)
                        expanded = false
                    }
                )
            }
        }
    }
}

// DropDown de Cliente
@Composable
fun locationDropdown(
    locations: List<Pair<Int, String>>, // Lista de monedas (id, name)
    onLocationtSelected: (Int) -> Unit // Callback con el ID de la moneda seleccionada
) {
    var expanded by remember { mutableStateOf(false) }
    var selectedLocation by remember { mutableStateOf<Pair<Int, String>?>(null) }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .border(2.dp, MoradoApp, shape = RoundedCornerShape(8.dp))
            .clickable { expanded = true }
            .padding(12.dp),
        contentAlignment = Alignment.CenterStart
    ) {
        Text(
            text = selectedLocation?.second ?: "Seleccione la moneda",
            style = AppTypography.labelLarge
        )

        Icon(
            imageVector = Icons.Default.ArrowDropDown,
            contentDescription = "Desplegar",
            modifier = Modifier.align(Alignment.CenterEnd)
        )

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            locations.forEach { location ->
                DropdownMenuItem(
                    text = { Text(location.second) },
                    onClick = {
                        selectedLocation = location
                        onLocationtSelected(location.first)
                        expanded = false
                    }
                )
            }
        }
    }
}

//Componente Listar Pedido
@Composable
fun PedidoBox(
    pedido: PedidoClass
) {
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
            // Crear la "cuadrícula" con filas y columnas alineadas
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = pedido.name, // Nombre del pedido a la izquierda
                    style = AppTypography.labelMedium,
                    modifier = Modifier
                        .weight(1f)
                        .padding(4.dp)
                        .align(Alignment.CenterVertically),
                    textAlign = TextAlign.Center
                )

                Text(
                    text = "Estado: ${pedido.state}", // Estado a la derecha
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
                    text = pedido.client.name,
                    style = AppTypography.labelMedium,
                    modifier = Modifier
                        .weight(1f)
                        .padding(4.dp)
                        .align(Alignment.CenterVertically),
                    textAlign = TextAlign.Center
                )
                Text(
                    text = "Total: $${pedido.price}",
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




@Composable
fun newAgregarButton(
    onClick: () -> Unit,
    nombre: String,
    buttonWidth: Dp = 200.dp // 🔹 Ancho definido por defecto en 200.dp
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isHovered by interactionSource.collectIsHoveredAsState()
    val buttonColor = VerdeApp
    val hoverColor = buttonColor.copy(alpha = 1f).compositeOver(Color.Black.copy(alpha = 0.3f))
    val currentColor = if (isHovered) hoverColor else buttonColor

    Box(
        modifier = Modifier
            .width(buttonWidth) // 🔹 Ancho fijo en lugar de fillMaxWidth()
            .border(2.dp, MoradoApp, RoundedCornerShape(12.dp))
    ) {
        // Sombra debajo del botón
        Box(
            modifier = Modifier
                .width(buttonWidth) // 🔹 Ancho fijo
                .height(4.dp)
                .background(Color.Black.copy(alpha = 0.3f))
                .align(Alignment.BottomCenter)
                .clip(RoundedCornerShape(12.dp))
                .offset(y = 2.dp)
        )

        // Fondo del botón
        Box(
            modifier = Modifier
                .width(buttonWidth) // 🔹 Ancho fijo
                .padding(bottom = 4.dp)
                .clip(RoundedCornerShape(12.dp))
                .background(currentColor)
        ) {
            Button(
                onClick = onClick,
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.Transparent // Botón transparente
                ),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .width(buttonWidth) // 🔹 Ancho fijo
                    .semantics { contentDescription = nombre },
                interactionSource = interactionSource
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Start
                ) {
                    Box(
                        modifier = Modifier.fillMaxWidth(),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = nombre,
                            style = AppTypography.labelLarge
                        )
                    }
                }
            }
        }

        if (isHovered) {
            Box(
                modifier = Modifier
                    .width(buttonWidth) // 🔹 Ancho fijo
                    .matchParentSize()
                    .background(Color.Black.copy(alpha = 0.3f))
                    .clip(RoundedCornerShape(12.dp))
            )
        }
    }
}


@Composable
fun newDualButton(
    nombreIzquierdo: String,
    onClickIzquierdo: () -> Unit,
    nombreDerecho: String,
    onClickDerecho: () -> Unit,
    buttonWidth: Dp = 200.dp,
    colorIzquierdo: Color = AmarilloApp,
    colorDerecho: Color = RojoApp
) {
    val interactionSourceIzq = remember { MutableInteractionSource() }
    val isHoveredIzq by interactionSourceIzq.collectIsHoveredAsState()

    val interactionSourceDer = remember { MutableInteractionSource() }
    val isHoveredDer by interactionSourceDer.collectIsHoveredAsState()

    val hoverColorIzq = colorIzquierdo.copy(alpha = 1f).compositeOver(Color.Black.copy(alpha = 0.3f))
    val hoverColorDer = colorDerecho.copy(alpha = 1f).compositeOver(Color.Black.copy(alpha = 0.3f))

    val currentColorIzq = if (isHoveredIzq) hoverColorIzq else colorIzquierdo
    val currentColorDer = if (isHoveredDer) hoverColorDer else colorDerecho

    Row(
        modifier = Modifier
            .width(buttonWidth)
            .height(48.dp)
            .border(2.dp, MoradoApp, RoundedCornerShape(30.dp))
    ) {
        // Botón izquierdo
        Box(
            modifier = Modifier
                .weight(1f)
                .padding(bottom = 4.dp)
                .clip(RoundedCornerShape(topStart = 30.dp, bottomStart = 30.dp))
                .background(currentColorIzq)
        ) {
            Button(
                onClick = onClickIzquierdo,
                colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent),
                shape = RoundedCornerShape(topStart = 30.dp, bottomStart = 30.dp),
                modifier = Modifier
                    .fillMaxSize()
                    .semantics { contentDescription = nombreIzquierdo },
                interactionSource = interactionSourceIzq
            ) {
                Text(
                    text = nombreIzquierdo,
                    style = AppTypography.labelLarge
                )
            }
        }

        // Botón derecho
        Box(
            modifier = Modifier
                .weight(1f)
                .padding(bottom = 4.dp)
                .clip(RoundedCornerShape(topEnd = 30.dp, bottomEnd = 30.dp))
                .background(currentColorDer)
        ) {
            Button(
                onClick = onClickDerecho,
                colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent),
                shape = RoundedCornerShape(topEnd = 30.dp, bottomEnd = 30.dp),
                modifier = Modifier
                    .fillMaxSize()
                    .semantics { contentDescription = nombreDerecho },
                interactionSource = interactionSourceDer
            ) {
                Text(
                    text = nombreDerecho,
                    style = AppTypography.labelLarge
                )
            }
        }
    }
}


@Composable
fun ListaDePedidos(pedidos: List<PedidoClass>) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(8.dp) // Espaciado entre elementos
    ) {
        items(pedidos) { pedido:PedidoClass  ->
            PedidoBox(pedido = pedido)
        }
    }
}


@Composable
fun ProductoPedidoBox(producto: ProductosPedidoClass) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 12.dp, vertical = 8.dp)
            .background(AmarilloApp, shape = RoundedCornerShape(8.dp))
            .border(2.dp, MoradoApp, shape = RoundedCornerShape(8.dp))
            .padding(8.dp), // Espaciado interno
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = producto.nombre,
            style = AppTypography.labelMedium,
            modifier = Modifier.weight(1f)
        )
        Text(
            text = "${producto.cantidadRequerida}",
            style = AppTypography.labelMedium,
            modifier = Modifier.weight(1f),
            textAlign = TextAlign.Center
        )
        Text(
            text = "$${producto.precioTotal}",
            style = AppTypography.labelMedium,
            modifier = Modifier.weight(1f),
            textAlign = TextAlign.End
        )
    }
}

@Composable
fun ListaDeProductosPedido(productos: List<ProductosPedidoClass>) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(productos) { producto ->
            ProductoPedidoBox(producto = producto)
        }
    }
}


@Composable
fun ProductoEditableBox(
    producto: ProductoClass,
    cantidadRequerida: Int,
    onCantidadChange: (Int) -> Unit
) {
    var cantidadTexto by remember { mutableStateOf(cantidadRequerida.toString()) }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(AmarilloApp, shape = RoundedCornerShape(8.dp))
            .border(2.dp, MoradoApp, shape = RoundedCornerShape(8.dp))
            .padding(12.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier.fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            // Primera línea: nombre y cantidad disponible
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = producto.name,
                    style = AppTypography.labelMedium,
                    modifier = Modifier.weight(1f),
                    textAlign = TextAlign.Start
                )
                Text(
                    text = "Disponible: ${producto.amount}",
                    style = AppTypography.labelMedium,
                    modifier = Modifier.weight(1f),
                    textAlign = TextAlign.End
                )
            }

            // Segunda línea: input y precio
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Input para cantidad requerida
                OutlinedTextField(
                    value = cantidadTexto,
                    onValueChange = { newValue ->
                        if (newValue.all { it.isDigit() }) {
                            cantidadTexto = newValue
                            onCantidadChange(newValue.toIntOrNull() ?: 0)
                        }
                    },
                    modifier = Modifier
                        .weight(1f)
                        .padding(end = 8.dp),
                    keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number),
                    singleLine = true
                )
                val cantidadActual = cantidadTexto.toIntOrNull() ?: 0
                val cantidadInvalida = cantidadActual > producto.amount
                Text(
                    text = "$${producto.price}",
                    style = AppTypography.labelMedium,
                    modifier = Modifier.weight(1f),
                    textAlign = TextAlign.End
                )
                // Precio unitario
                if (cantidadInvalida) {
                    Text(
                        text = "Cantidad excede disponible",
                        color = Color.Red,
                        style = AppTypography.labelSmall,
                        modifier = Modifier.align(Alignment.CenterVertically)
                    )
            }
        }

        }
    }
}

@Composable
fun ListaDeProductosEditable(
    productos: List<ProductoClass>,
    cantidades: Map<String, Int>,
    onCantidadChange: (String, Int) -> Unit
) {
    LazyColumn(
        verticalArrangement = Arrangement.spacedBy(8.dp),
        modifier = Modifier.fillMaxSize()
    ) {
        items(productos) { producto ->
            ProductoEditableBox(
                producto = producto,
                cantidadRequerida = cantidades[producto.id] ?: 0,
                onCantidadChange = { nuevaCantidad ->
                    onCantidadChange(producto.id, nuevaCantidad)
                }
            )
        }
    }
}



