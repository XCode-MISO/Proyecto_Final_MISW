package com.example.sigccp

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class CrearClienteE2eTest {
    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()
    private val robot = MainActivityRobot(composeTestRule)

    @Test
    fun testScreenCrearClienteSeMuestra() {
        robot.clickOnCrearCliente()
        robot.verificarScreenConTituloSeMuestra("Create Client")
        robot.clickEnBoton("Cancelar")
    }

}
