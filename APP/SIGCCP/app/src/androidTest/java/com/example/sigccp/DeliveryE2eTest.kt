package com.example.sigccp

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import org.junit.Rule
import org.junit.Test

class DeliveryE2eTest {
    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()
    private val robot = MainActivityRobot(composeTestRule)

    @Test
    fun deliverySeMuestraTest() {
        robot.escribirEnCampo("Correo", "cliente@gmail.com")
        robot.escribirEnCampo("Contraseña", "12345678")
        robot.clickEnBoton("Ingresar")
        robot.esperarProcesamiento(3000)
        robot.verificarScreenConTituloSeMuestra("¡Hello, Client!")
        robot.clickEnBoton("DELIVERY")
        robot.verificarScreenConTituloSeMuestra("DELIVERY")
        robot.clickEnBoton("logout")
        robot.esperarProcesamiento(500)
    }
}