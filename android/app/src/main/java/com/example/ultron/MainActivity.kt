package com.example.ultron

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.ultron.elements.MainFragment
import com.example.ultron.elements.PreferencesManager
import com.example.ultron.ui.theme.UltronTheme


class MainActivity : ComponentActivity() {
    private lateinit var preferenceManager:PreferencesManager
    private lateinit var urls: Map<String,*>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        preferenceManager = PreferencesManager(this)
        val prefs: SharedPreferences =
            this.getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)
        urls= prefs.all
        urls = urls.filterKeys { it!="serverUrl" }
        setContent {
            UltronTheme {
                MainFragment(preferenceManager, urls)
            }
        }
    }
}
