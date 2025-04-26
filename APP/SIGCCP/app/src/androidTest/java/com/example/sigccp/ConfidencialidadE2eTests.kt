package com.example.sigccp

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ConfidencialidadE2eTests {

    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()
    private val robot = MainActivityRobot(composeTestRule)

    @Test
    fun confidencialidadMenuVendedor() {
        robot.escribirEnCampo("Correo", "vendedor@gmail.com")
        robot.escribirEnCampo("Contraseña", "12345678")
        robot.clickEnBoton("Ingresar")
        robot.esperarProcesamiento(3000)
        robot.verificarScreenConTituloSeMuestra("¡Hello, Seller!")
        robot.botonEstaActivo("PEDIDOS")
        robot.botonEstaActivo("CLIENTES")
        robot.botonEstaActivo("INVENTARIO")
        robot.botonEstaActivo("RUTAS")
        robot.botonEstaActivo("RECOMENDACION")
        robot.botonEstaActivo("REGISTRAR VISITA")
        robot.clickEnBoton("logout")
        robot.esperarProcesamiento(500)
    }

    @Test
    fun confidencialidadMenuCliente() {
        robot.escribirEnCampo("Correo", "cliente@gmail.com")
        robot.escribirEnCampo("Contraseña", "12345678")
        robot.clickEnBoton("Ingresar")
        robot.esperarProcesamiento(3000)
        robot.verificarScreenConTituloSeMuestra("¡Hello, Client!")
        robot.botonEstaActivo("PEDIDOS")
        robot.botonNoEstaActivo("CLIENTES")
        robot.botonEstaActivo("INVENTARIO")
        robot.botonNoEstaActivo("RUTAS")
        robot.botonNoEstaActivo("RECOMENDACION")
        robot.botonNoEstaActivo("REGISTRAR VISITA")
        robot.clickEnBoton("logout")
        robot.esperarProcesamiento(500)
    }

}