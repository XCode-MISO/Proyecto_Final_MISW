package com.example.sigccp

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import org.junit.Rule
import org.junit.Test

class ListarRutasTest {
    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()
    private val robot = MainActivityRobot(composeTestRule)

    @Test
    fun ListarRutasFuncionaTest() {
        robot.esperarProcesamiento(2000)
        composeTestRule.waitForIdle()

        // Selección de idioma e inicio de sesión
        robot.seleccionarIdiomaIngles(composeTestRule)
        robot.esperarProcesamiento(2000)
        robot.escribirEnCampo("Correo", "vendedor@gmail.com")
        robot.escribirEnCampo("Contraseña", "12345678")
        robot.clickEnBoton("Ingresar")
        robot.esperarProcesamiento(3000)

        // Verificación pantalla principal
        robot.verificarScreenConTituloSeMuestra("¡Hello, Seller!")

        // Navegar a la pantalla de rutas
        robot.clickEnBoton("ROUTES") // testTag en botón para navegar a rutas

        robot.esperarProcesamiento(6000)
        // Verificación del título de la pantalla
        robot.verificarScreenConTituloSeMuestra("ROUTES") // Ajustar según stringResource(R.string.listRoutes)

        // Verificar que está visible el selector de fecha
        robot.botonEstaVisible("SelectorFecha") // testTag en el Box clickable que abre el DatePicker
        robot.esperarProcesamiento(6000)
        composeTestRule
            .onNodeWithTag("ruta_1")
            .performClick()

        robot.esperarProcesamiento(3000)
        robot.verificarScreenConTituloSeMuestra("ROUTE") // Ajusta el título según corresponda

    }
}