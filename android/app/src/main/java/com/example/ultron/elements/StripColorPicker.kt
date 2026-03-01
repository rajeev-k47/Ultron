package com.example.ultron.elements

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.godaddy.android.colorpicker.ClassicColorPicker
import com.godaddy.android.colorpicker.HsvColor

@Composable
fun StripColorPicker(server: String) {
    var selectedColor by remember {
        mutableStateOf(HsvColor.from(Color.Red))
    }

    ClassicColorPicker(
        modifier = Modifier
            .fillMaxWidth()
            .height(300.dp).padding(10.dp),
        color = selectedColor,
        showAlphaBar = false,
        onColorChanged = { newColor: HsvColor ->
            val composeColor = newColor.toColor()
            val r = (composeColor.red * 255).toInt()
            val g = (composeColor.green * 255).toInt()
            val b = (composeColor.blue * 255).toInt()
            makeRequest(server+"strip/color?r=$r&g=$g&b=$b")

        }
    )
}