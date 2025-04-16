package com.example.sigccp

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.ComposeTestRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performTextInput
import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking

class MainActivityRobot(private val composeTestRule: ComposeTestRule) {
    fun clickOnCrearCliente() {
        composeTestRule
            .onNodeWithText("Crear Cliente")
            .performClick()
    }

    // Function to verify if an investment card is displayed based on its tag
    fun verificarScreenConTituloSeMuestra(text: String) {
        composeTestRule
            .onNodeWithText(text)
            .assertIsDisplayed()
    }

    fun escribirEnCampo(tag: String, texto: String) {
        composeTestRule
            .onNodeWithTag(tag)
            .performTextInput(texto)
    }

    fun clickEnBoton(tag: String){
        composeTestRule
            .onNodeWithTag(tag)
            .performClick()
    }

    fun esperarProcesamiento(segundos: Long){
        runBlocking { delay(segundos) }
    }

}