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
        robot.esperarProcesamiento(2000)
        composeTestRule.waitForIdle()

        // Ejecutar la función
        robot.seleccionarIdiomaIngles(composeTestRule)
        robot.esperarProcesamiento(2000)
        robot.escribirEnCampo("Correo", "vendedor@gmail.com")
        robot.escribirEnCampo("Contraseña", "12345678")
        robot.clickEnBoton("Ingresar")
        robot.esperarProcesamiento(3000)
        robot.verificarScreenConTituloSeMuestra("¡Hello, Seller!")
        robot.botonEstaVisible("ORDERS")
        robot.botonEstaVisible("CLIENTS")
        robot.botonEstaVisible("ROUTES")
        robot.botonEstaVisible("ADVICE")
        robot.botonEstaVisible("REGISTER VISIT")
        robot.botonNoEstaVisible("DELIVERY")
        robot.clickEnBoton("logout")
        robot.esperarProcesamiento(500)
    }

    @Test
    fun confidencialidadMenuCliente() {
        robot.esperarProcesamiento(2000)
        composeTestRule.waitForIdle()

        // Ejecutar la función
        robot.seleccionarIdiomaIngles(composeTestRule)
        robot.esperarProcesamiento(2000)
        robot.escribirEnCampo("Correo", "cliente@gmail.com")
        robot.escribirEnCampo("Contraseña", "12345678")
        robot.clickEnBoton("Ingresar")
        robot.esperarProcesamiento(3000)
        robot.verificarScreenConTituloSeMuestra("¡Hello, Client!")
        robot.botonEstaVisible ("ORDERS")
        robot.botonEstaVisible("DELIVERY")
        robot.botonNoEstaVisible("CLIENTS")
        robot.botonNoEstaVisible("ROUTES")
        robot.botonNoEstaVisible("ADVICE")
        robot.botonNoEstaVisible("REGISTER VISIT")
        robot.clickEnBoton("logout")
        robot.esperarProcesamiento(500)
    }
}