package com.example.sigccp

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertIsEnabled
import androidx.compose.ui.test.assertIsNotDisplayed
import androidx.compose.ui.test.assertIsNotEnabled
import androidx.compose.ui.test.junit4.ComposeTestRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithContentDescription
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

    fun seleccionarIdiomaIngles(composeTestRule: ComposeTestRule) {
        // Hacer clic en el icono del idioma para abrir el dropdown
        composeTestRule.onNodeWithContentDescription("Idioma").performClick()

        // Esperar hasta que aparezca al menos un nodo "EN"
        composeTestRule.waitUntil(timeoutMillis = 3_000) {
            composeTestRule.onAllNodesWithText("EN", useUnmergedTree = true)
                .fetchSemanticsNodes().isNotEmpty()
        }

        // Obtener todos los nodos con texto "EN"
        val enNodes = composeTestRule.onAllNodesWithText("EN", useUnmergedTree = true)

        if (enNodes.fetchSemanticsNodes().size >= 2) {
            // Si hay 2 o más "EN", hacer clic en el segundo (índice 1)
            enNodes[1].performClick()
        } else {
            // Si solo hay uno, hacer clic en ese
            enNodes[0].performClick()
        }

        esperarProcesamiento(2000)
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

    fun botonEstaActivo(tag: String){
        composeTestRule
            .onNodeWithTag(tag)
            .assertIsEnabled()
    }

    fun botonNoEstaActivo(tag: String){
        composeTestRule
            .onNodeWithTag(tag)
            .assertIsNotEnabled()
    }

    fun botonEstaVisible(tag: String) {
        composeTestRule
            .onNodeWithTag(tag)
            .assertIsDisplayed()
    }

    fun botonNoEstaVisible(tag: String) {
        composeTestRule
            .onNodeWithTag(tag)
            .assertIsNotDisplayed()
    }

}