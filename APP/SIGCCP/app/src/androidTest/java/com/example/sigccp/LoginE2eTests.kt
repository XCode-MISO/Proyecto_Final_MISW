package com.example.sigccp

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class LoginE2eTests {
    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()
    private val robot = MainActivityRobot(composeTestRule)

    @Test
    fun testScreenCrearClienteSeMuestra() {
        robot.esperarProcesamiento(2000)
        composeTestRule.waitForIdle()

        // Ejecutar la función
        robot.seleccionarIdiomaIngles(composeTestRule)
        robot.esperarProcesamiento(2000)
        robot.clickOnCrearCliente()
        robot.verificarScreenConTituloSeMuestra("Create Client")
        robot.clickEnBoton("Cancelar")
    }

    @Test
    fun loginClienteCorrectoTest() {
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
        robot.clickEnBoton("logout")
        robot.esperarProcesamiento(500)
    }

    @Test
    fun loginVendedorCorrectoTest() {
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
        robot.clickEnBoton("logout")
        robot.esperarProcesamiento(500)
    }
}
