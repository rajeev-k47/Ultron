package com.example.ultron.widgets

import android.content.Context
import android.content.SharedPreferences
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.glance.Button
import androidx.glance.ButtonColors
import androidx.glance.ButtonDefaults
import androidx.glance.GlanceId
import androidx.glance.GlanceModifier
import androidx.glance.LocalContext
import androidx.glance.appwidget.GlanceAppWidget
import androidx.glance.appwidget.cornerRadius
import androidx.glance.appwidget.provideContent
import androidx.glance.background
import androidx.glance.layout.Alignment
import androidx.glance.layout.Box
import androidx.glance.layout.Column
import androidx.glance.layout.Row
import androidx.glance.layout.fillMaxSize
import androidx.glance.layout.padding
import androidx.glance.text.FontWeight
import androidx.glance.text.Text
import androidx.glance.text.TextStyle
import androidx.glance.unit.ColorProvider
import com.example.ultron.elements.PreferencesManager
import com.example.ultron.elements.makeRequest
import com.example.ultron.ui.theme.BackgroundColor

class RequestWidget: GlanceAppWidget() {
    private lateinit var urls: Map<String,*>
    override suspend fun provideGlance(context: Context, id: GlanceId) {
        var preferenceManager = PreferencesManager(context)

        val prefs: SharedPreferences =
            context.getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)
        urls= prefs.all
        urls = urls.filterKeys { it=="serverUrl" }
        provideContent {
            MyContent(urls["serverUrl"].toString())
        }
    }


    @Composable
    private fun MyContent(server: String?="") {
        Column(
            modifier = GlanceModifier.background(BackgroundColor),
            verticalAlignment = Alignment.Top,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Box(
                modifier = GlanceModifier
                    .background(Color.Red)
                    .padding(3.dp),
                contentAlignment = Alignment.Center
            ) {
                Button(
                    text = "Tube Light",
                    style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp),
                    onClick = {
                            makeRequest(server+ "tubelight/") //harcoded!!
                    },
                    colors = ButtonDefaults.buttonColors(
                        backgroundColor = ColorProvider(Color.Black),
                        contentColor = ColorProvider(Color.Red)
                    )
                )
            }
        }
    }
}