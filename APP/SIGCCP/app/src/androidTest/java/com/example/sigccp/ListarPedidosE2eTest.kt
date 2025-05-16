package com.example.sigccp

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ListarPedidosE2eTest {
    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()
    private val robot = MainActivityRobot(composeTestRule)

    @Test
    fun listarPedidosSeMuestraTest() {
        robot.esperarProcesamiento(2000)
        composeTestRule.waitForIdle()

        // Ejecutar la función
        robot.seleccionarIdiomaIngles(composeTestRule)
        robot.esperarProcesamiento(2000)
        // Iniciar sesión
        robot.escribirEnCampo("Correo", "cliente@gmail.com")
        robot.escribirEnCampo("Contraseña", "12345678")
        robot.clickEnBoton("Ingresar")
        robot.esperarProcesamiento(3000)

        // Verificar pantalla principal de cliente
        robot.verificarScreenConTituloSeMuestra("¡Hello, Client!")

        // Ir a la vista de pedidos
        robot.clickEnBoton("ORDERS") // Asegúrate que este botón tenga el testTag="Pedidos"
        robot.esperarProcesamiento(2000)

        // Verificar que estamos en la vista de Listar Pedidos
        robot.verificarScreenConTituloSeMuestra("¡Your Orders!") // Ajusta según el string exacto en strings.xml

        // Verificar que el botón "Crear Pedido" está presente
        robot.botonEstaVisible("Crear Pedido") // Asegúrate que el botón tenga testTag="Crear Pedido"

        // Clic en "Crear Pedido" para verificar navegación
        robot.clickEnBoton("Crear Pedido")
        robot.esperarProcesamiento(2000)

        // Verificar que se muestra la pantalla de creación de pedido
        robot.verificarScreenConTituloSeMuestra("¡Your Order!") // Ajusta el título según corresponda
    }
}
