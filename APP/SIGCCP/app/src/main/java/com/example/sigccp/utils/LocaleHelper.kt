package com.example.sigccp.utils

import android.content.Context
import android.content.res.Configuration
import java.util.Locale

fun setAppLocale(context: Context, language: String) {
    val locale = Locale(language)
    Locale.setDefault(locale)
    val config = Configuration()
    config.setLocale(locale)
    context.resources.updateConfiguration(config, context.resources.displayMetrics)

    // Guardar idioma en SharedPreferences
    val sharedPref = context.getSharedPreferences("AppSettings", Context.MODE_PRIVATE)
    sharedPref.edit().putString("LANGUAGE", language).apply()
}

fun getSavedLanguage(context: Context): String {
    val sharedPref = context.getSharedPreferences("AppSettings", Context.MODE_PRIVATE)
    return sharedPref.getString("LANGUAGE", "es") ?: "es" // "es" como predeterminado
}
