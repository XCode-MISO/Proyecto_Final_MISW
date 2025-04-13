package com.example.sigccp

import android.content.Context
import android.content.SharedPreferences

object PreferenceKeys {
    const val ROLE = "role"
    const val TOKEN = "token"
    const val USER_ID = "userId"
    const val USER_NAME = "userName"
}

object PreferencesManager { // Change to 'object'

    private const val PREFERENCE_FILE_KEY = "userData"
    private var INSTANCE: SharedPreferences? = null

    fun init(context: Context) {
        if (INSTANCE == null) {
            INSTANCE = context.getSharedPreferences(PREFERENCE_FILE_KEY, Context.MODE_PRIVATE)
        }
    }

    private fun getInstance(): SharedPreferences {
        return INSTANCE ?: throw IllegalStateException("PreferencesManager not initialized. Call init() first.")
    }

    fun saveString(key: String, value: String) {
        val editor = getInstance().edit()
        editor.putString(key, value)
        editor.apply()
    }

    fun getString(key: String, defaultValue: String = ""): String {
        return getInstance().getString(key, defaultValue) ?: defaultValue
    }

    fun saveBoolean(key: String, value: Boolean) {
        val editor = getInstance().edit()
        editor.putBoolean(key, value)
        editor.apply()
    }

    fun getBoolean(key: String, defaultValue: Boolean = false): Boolean {
        return getInstance().getBoolean(key, defaultValue)
    }

    fun clearAll() {
        val editor = getInstance().edit()
        editor.clear()
        editor.apply()
    }

    fun remove(key: String) {
        val editor = getInstance().edit()
        editor.remove(key)
        editor.apply()
    }
}