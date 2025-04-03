package com.example.sigccp.utils

import android.app.Activity
import android.content.Context
import android.content.res.Configuration
import android.os.Handler
import android.os.Looper
import androidx.core.app.ActivityCompat
import java.util.Locale

fun setAppLocale(activity: Activity?, language: String) {
    activity?.let {
        val locale = Locale(language)
        Locale.setDefault(locale)

        val config = Configuration(it.resources.configuration)
        config.setLocale(locale)

        // Usar el nuevo contexto de configuración sin afectar la interfaz de usuario
        it.applicationContext.createConfigurationContext(config)
    }
}

// RestartActivity para internacionalización
fun restartActivity(activity: Activity?) {
    activity?.let {
        Handler(Looper.getMainLooper()).postDelayed({
            ActivityCompat.recreate(it)
        }, 100) // Pequeño retraso para evitar la interrupción brusca de la UI
    }
}

fun getSavedLanguage(context: Context): String {
    val sharedPref = context.getSharedPreferences("AppSettings", Context.MODE_PRIVATE)
    return sharedPref.getString("LANGUAGE", "es") ?: "es" // "es" como predeterminado
}

fun saveLanguage(context: Context, language: String) {
    val sharedPref = context.getSharedPreferences("AppSettings", Context.MODE_PRIVATE)
    with(sharedPref.edit()) {
        putString("LANGUAGE", language)
        apply()
    }
}